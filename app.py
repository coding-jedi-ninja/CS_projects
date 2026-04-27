from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
from typing import Optional

from backend.menu import Menu
from backend.order import Order
from backend.inventory_ShuranRyu import Inventory
from backend.customer import Customer, Customers
from backend.staff import Staffs

app = FastAPI(title="Campus Café API")

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (same as main.py)
menu = Menu()
order = Order(menu)
staffs = Staffs()
session_orders = {}


# --- Pydantic request models ---

class CartAddRequest(BaseModel):
    item_name: str
    quantity: int


class CartRemoveRequest(BaseModel):
    item_name: str
    quantity: int


class CheckoutRequest(BaseModel):
    telephone: int


class StaffLoginRequest(BaseModel):
    staff_id: str
    password: str


class RestockRequest(BaseModel):
    item_name: str
    amount: int


class StaffCreateRequest(BaseModel):
    name: str
    telephone: str
    password: str


class StaffUpdateRequest(BaseModel):
    name: Optional[str] = None
    telephone: Optional[str] = None
    password: Optional[str] = None


# --- Menu endpoints ---

@app.get("/api/menu")
def get_menu(category: str = Query(None)):
    items = []
    for item in menu.menu:
        if category and item.category.lower() != category.lower():
            continue
        items.append({
            "name": item.name,
            "price": item.price,
            "category": item.category,
            "is_special": item == menu.special_item,
        })

    return {
        "items": items,
        "daily_special": {
            "name": menu.special_item.name,
            "discount_rate": menu.special_discounted_rate,
        },
        "categories": list({item.category for item in menu.menu}),
    }


# --- Cart endpoints ---

@app.get("/api/cart")
def get_cart():
    items_num = order.get_items_num()
    cart_items = []
    for item, qty in items_num.items():
        cart_items.append({
            "name": item.name,
            "price": item.price,
            "quantity": qty,
            "subtotal": round(item.price * qty, 2),
            "is_special": item == menu.special_item,
        })

    subtotal = round(order.get_total(), 2)
    total_after_discount = round(order.get_total_after_discount(), 2)
    discount = round(subtotal - total_after_discount, 2)
    tax = round(order.TAX_RATE * total_after_discount, 2)
    total = round(total_after_discount + tax, 2)

    return {
        "items": cart_items,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
    }


@app.post("/api/cart/add")
def add_to_cart(req: CartAddRequest):
    item = menu.get_item(req.item_name)
    if item is None:
        return {"success": False, "message": "Item not found."}

    inventory = Inventory()
    added = 0
    for _ in range(req.quantity):
        if inventory.check_stock(item):
            order.add_to_order(item)
            inventory.deduct_stock(item)
            inventory.save_to_excel()
            added += 1
        else:
            break

    if added == 0:
        return {"success": False, "message": f"Sorry, {item.name} is out of stock.", "added": 0}

    msg = f"You have ordered {added} {item.name}."
    if added < req.quantity:
        msg += f" (Only {added} available)"

    return {"success": True, "message": msg, "added": added}


@app.post("/api/cart/remove")
def remove_from_cart(req: CartRemoveRequest):
    item = menu.get_item(req.item_name)
    if item is None:
        return {"success": False, "message": "Item not found."}

    if item not in order.items:
        return {"success": False, "message": "You didn't order this item."}

    items_num = order.get_items_num()
    num_max = min(req.quantity, items_num.get(item, 0))

    for _ in range(num_max):
        order.remove_from_order(item)
        inventory = Inventory()
        inventory.restore_stock(item)
        inventory.save_to_excel()

    return {"success": True, "message": f"You have deleted {num_max} {item.name}.", "removed": num_max}


@app.post("/api/cart/clear")
def clear_cart():
    # Restore all inventory
    inventory = Inventory()
    for item in order.items:
        inventory.restore_stock(item)
    inventory.save_to_excel()
    order.clear_order()
    return {"success": True, "message": "Cart cleared."}


# --- Checkout endpoint ---

@app.post("/api/checkout")
def checkout(req: CheckoutRequest):
    if len(order.items) == 0:
        return {"success": False, "message": "Sorry, you didn't order anything."}

    subtotal = round(order.get_total(), 2)
    total_before_tax = round(order.get_total_after_discount(), 2)
    discount = round(subtotal - total_before_tax, 2)
    tax = round(order.TAX_RATE * total_before_tax, 2)
    total = round(total_before_tax + tax, 2)

    # Customer loyalty points
    customers = Customers()
    if customers.check_customer(req.telephone):
        customer = customers.get_customer(req.telephone)
        customer.earn_points(total)
        customers.update_customer(customer)
    else:
        customer = Customer(req.telephone)
        customer.earn_points(total)
        customers.add_customer(customer)

    customers.save_to_excel()

    # Build receipt items
    items_num = order.get_items_num()
    receipt_items = []
    for item, qty in items_num.items():
        receipt_items.append({
            "name": item.name,
            "quantity": qty,
            "price": round(item.price * qty, 2),
        })

    now = datetime.now()

    # Save order and record in session
    order.save_to_excel()
    session_orders[len(session_orders)] = {"Total": total, "Items": str(order), "receipt_items": receipt_items}
    order.clear_order()

    return {
        "success": True,
        "receipt": {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "customer_id": customer.customer_id,
            "points": customer.points,
            "items": receipt_items,
            "subtotal": subtotal,
            "discount": discount,
            "tax": tax,
            "total": total,
        },
    }


# --- Staff endpoints ---

@app.post("/api/staff/login")
def staff_login(req: StaffLoginRequest):
    if not staffs.check_staff(req.staff_id):
        return {"success": False, "message": "Invalid staff ID."}

    staff = staffs.get_staff(req.staff_id)
    if staff.password != req.password:
        return {"success": False, "message": "Invalid password."}

    return {"success": True, "name": staff.name}


@app.get("/api/staff")
def get_staff_accounts():
    return {"items": staffs.list_staffs()}


@app.post("/api/staff")
def create_staff_account(req: StaffCreateRequest):
    if not req.name.strip():
        return {"success": False, "message": "Staff name is required."}
    if not req.telephone.strip().isdigit() or int(req.telephone) <= 0:
        return {"success": False, "message": "Telephone must be a positive number."}
    if not req.password.strip():
        return {"success": False, "message": "Password is required."}

    staff = staffs.create_staff(req.name, req.telephone, req.password)
    staffs.save_to_excel()
    return {
        "success": True,
        "message": f"Staff account created for {staff.name}.",
        "staff": staff.to_dict(),
    }


@app.put("/api/staff/{staff_id}")
def update_staff_account(staff_id: str, req: StaffUpdateRequest):
    if not staffs.check_staff(staff_id):
        return {"success": False, "message": "Staff ID not found."}

    if req.telephone is not None and (
        not req.telephone.strip().isdigit() or int(req.telephone) <= 0
    ):
        return {"success": False, "message": "Telephone must be a positive number."}

    if req.name is not None and not req.name.strip():
        return {"success": False, "message": "Staff name cannot be empty."}

    if req.password is not None and not req.password.strip():
        return {"success": False, "message": "Password cannot be empty."}

    staff = staffs.update_staff_record(
        staff_id,
        name=req.name,
        telephone=req.telephone,
        password=req.password,
    )
    staffs.save_to_excel()
    return {
        "success": True,
        "message": f"Staff account {staff_id} updated.",
        "staff": staff.to_dict(),
    }


@app.delete("/api/staff/{staff_id}")
def delete_staff_account(staff_id: str):
    if not staffs.check_staff(staff_id):
        return {"success": False, "message": "Staff ID not found."}
    if len(staffs.staffs) == 1:
        return {
            "success": False,
            "message": "At least one staff account must remain in the system.",
        }

    staff = staffs.get_staff(staff_id)
    staffs.delete_staff_by_id(staff_id)
    staffs.save_to_excel()
    return {"success": True, "message": f"Staff account deleted for {staff.name}."}


@app.get("/api/inventory")
def get_inventory():
    inventory = Inventory()
    items = []
    for name, qty in inventory.stock.items():
        items.append({"name": name, "quantity": int(qty)})
    return {"items": items}


@app.post("/api/inventory/restock")
def restock(req: RestockRequest):
    inventory = Inventory()
    if req.item_name not in inventory.stock:
        return {"success": False, "message": "Item not found in inventory."}

    inventory.restock(req.item_name, req.amount)
    inventory.save_to_excel()
    return {"success": True, "message": f"You have restocked {req.amount} {req.item_name}s."}


# --- Session endpoints ---

@app.get("/api/session/orders")
def get_session_orders():
    orders = []
    total_revenue = 0
    for idx, info in session_orders.items():
        orders.append({"order_id": idx, "total": info["Total"], "items": info["Items"], "receipt_items": info.get("receipt_items", [])})
        total_revenue += info["Total"]

    return {
        "orders": orders,
        "order_count": len(session_orders),
        "total_revenue": round(total_revenue, 2),
    }


@app.post("/api/session/quit")
def session_quit():
    result = get_session_orders()
    session_orders.clear()
    # Refresh daily special for the next session
    menu.special_item = menu.daily_special()
    return result


if FRONTEND_DIST.exists():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="frontend-assets")

    @app.get("/favicon.svg", include_in_schema=False)
    def frontend_favicon():
        return FileResponse(FRONTEND_DIST / "favicon.svg")

    @app.get("/icons.svg", include_in_schema=False)
    def frontend_icons():
        return FileResponse(FRONTEND_DIST / "icons.svg")

    @app.get("/", include_in_schema=False)
    def frontend_index():
        return FileResponse(FRONTEND_DIST / "index.html")

    @app.get("/{full_path:path}", include_in_schema=False)
    def frontend_spa(full_path: str):
        return FileResponse(FRONTEND_DIST / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
