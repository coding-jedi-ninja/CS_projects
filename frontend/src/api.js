const BASE = '/api';

export async function fetchMenu(category) {
  const url = category ? `${BASE}/menu?category=${category}` : `${BASE}/menu`;
  const res = await fetch(url);
  return res.json();
}

export async function fetchCart() {
  const res = await fetch(`${BASE}/cart`);
  return res.json();
}

export async function addToCart(itemName, quantity) {
  const res = await fetch(`${BASE}/cart/add`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ item_name: itemName, quantity }),
  });
  return res.json();
}

export async function removeFromCart(itemName, quantity) {
  const res = await fetch(`${BASE}/cart/remove`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ item_name: itemName, quantity }),
  });
  return res.json();
}

export async function clearCart() {
  const res = await fetch(`${BASE}/cart/clear`, { method: 'POST' });
  return res.json();
}

export async function checkout(telephone) {
  const res = await fetch(`${BASE}/checkout`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ telephone }),
  });
  return res.json();
}

export async function staffLogin(staffId, password) {
  const res = await fetch(`${BASE}/staff/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ staff_id: staffId, password }),
  });
  return res.json();
}

export async function fetchInventory() {
  const res = await fetch(`${BASE}/inventory`);
  return res.json();
}

export async function fetchStaffAccounts() {
  const res = await fetch(`${BASE}/staff`);
  return res.json();
}

export async function createStaffAccount(payload) {
  const res = await fetch(`${BASE}/staff`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function updateStaffAccount(staffId, payload) {
  const res = await fetch(`${BASE}/staff/${staffId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function deleteStaffAccount(staffId) {
  const res = await fetch(`${BASE}/staff/${staffId}`, {
    method: 'DELETE',
  });
  return res.json();
}

export async function restockItem(itemName, amount) {
  const res = await fetch(`${BASE}/inventory/restock`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ item_name: itemName, amount }),
  });
  return res.json();
}

export async function fetchSessionOrders() {
  const res = await fetch(`${BASE}/session/orders`);
  return res.json();
}

export async function sessionQuit() {
  const res = await fetch(`${BASE}/session/quit`, { method: 'POST' });
  return res.json();
}
