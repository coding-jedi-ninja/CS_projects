# Campus Cafe Change Summary

## What Changed

This refresh focused on three goals:

1. Make the project more compliant with the CS5001 shared contract and final-demo rubric.
2. Keep the presentation code snippets aligned with the latest working code.
3. Clean up the integrated Inventory implementation so it is easier to explain, test, and demo.

## Contract Compliance Improvements

### `main.py`

- The main menu now follows the required customer flow more closely:
  - `[1] View menu`
  - `[2] Order item`
  - `[3] View cart`
  - `[4] Checkout`
  - `[s] Staff mode (bonus feature)`
  - `[q] Quit`
- This directly supports the professor's required demo sequence from the Student Guide.
- Invalid menu input is handled cleanly with a helpful re-prompt.
- Empty-cart checkout still returns gracefully without printing a fake $0 receipt.

### `backend/menu.py`

- Reintroduced contract-compatible module-level symbols:
  - `MENU`
  - `display_menu(menu)`
  - `get_item(menu, name)`
- These wrappers now work alongside the richer `Menu` class instead of replacing it.
- Added `_normalize_name()` so lookups stay case-insensitive and space-insensitive.
- Improved `display_menu(menu)` so it no longer depends on instantiating a fresh `Menu()` object just to print grouped items.

### `backend/order.py`

- Kept the required order contract methods in place while improving clarity and persistence handling.
- `save_to_excel()` now clearly uses `data_file()` so persistence logic is aligned with the deployed app as well as the local app.
- Simplified repeated counting by reusing `get_items_num()`.

### `backend/inventory_ShuranRyu.py`

- Preserved the required inventory contract methods:
  - `check_stock(item)`
  - `deduct_stock(item)`
  - `restock(item_name, amount)`
  - `stock_report()`
- Added integration helpers that made the class usable in the full app:
  - `restore_stock(item)`
  - `load_from_excel()`
  - `save_to_excel()`
- Updated persistence to use `data_file()` so the same code works with local files and deployed seed data.

## Shuran And Ryu Inventory Integration Analysis

### What We Reused

- Their Week 1 inventory design followed the shared contract closely.
- The stock structure was simple and reliable: a dictionary from item name to quantity.
- `check_stock()` and `deduct_stock()` already matched the expected order workflow.
- `restock()` fit naturally into the bonus staff mode.

### What We Had To Change

- The original file used a hard-coded stock dictionary instead of shared data files.
- The original file used a local `Item` test class instead of the real `MenuItem` objects from our app.
- The original implementation printed stock messages directly inside `check_stock()`.
- There was no built-in way to restore stock when an item was deleted from the cart.
- File access assumed a simple local `data/` path, which was too fragile once we added deployment and seeded files.

### Why These Changes Mattered

- The terminal app needed `check_stock()` to behave like a reusable boolean guard, not a print-heavy UI function.
- The cart delete flow needed `restore_stock(item)` or the inventory would drift out of sync.
- Both the FastAPI backend and the terminal app needed to read and write the same inventory logic.
- The deployment-safe `data_file()` helper made the code more portable and more consistent across local and hosted runs.

## Presentation Snippet Updates

The presentation deck was updated so the code screenshots better match the current codebase.

### Updated slides

- `Slide 8`: updated `main_menu()` snippet to show the correct `1/2/3/4/q` flow and the hidden `staff` branch.
- `Slide 15`: replaced stale menu persistence snippet with the contract-compatible `MENU`, `display_menu(menu)`, and `get_item(menu, name)` wrappers.
- `Slide 18`: updated `Order.save_to_excel()` snippet to use `data_file()` and clearer order ID logic.
- `Slides 19-21`: refreshed the Inventory snippets to match the current integrated version and the persistence helper.
- `Slide 22`: added a new inventory integration analysis slide so the challenges/fixes story is easier to read and less cluttered.
- `Slide 25` in the updated deck (shifted after slide insertion): updated the Customer persistence snippet to use `data_file()`.

## Code Quality Improvements

- Added clearer docstrings and comments to the refreshed code files.
- Removed several confusing old comments from the adapted Inventory implementation.
- Made policy-related logic clearer in `Customer.earn_points()` and `Customer.use_points()`.
- Added safer stock restoration logic in Inventory with `get(..., 0) + 1`.
- Improved menu formatting and lookup reuse in `backend/menu.py`.

## Deployment And Data Consistency Improvements

- Synced the public demo staff credentials with local data so the same staff login works in both environments.
- Kept the deployed app aligned with the seeded demo data expected by the public frontend.

## Test Status

- The refreshed code package in `outputs/campus-cafe-final-code/` passed `python3 -m py_compile` for:
  - `main.py`
  - `app.py`
  - `backend/menu.py`
  - `backend/order.py`
  - `backend/inventory_ShuranRyu.py`
  - `backend/customer.py`
  - `backend/staff.py`
  - `backend/paths.py`

## Main Compliance Takeaway

The project now does a better job of satisfying the professor's rubric because it:

- demonstrates the required CLI menu flow more clearly,
- keeps the shared contract visible in the code,
- handles the required Week 3 edge cases safely,
- explains external code integration with concrete examples,
- and keeps the presentation code snippets aligned with the actual working implementation.
