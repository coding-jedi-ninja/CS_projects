import { useEffect, useState } from 'react'
import {
  createStaffAccount,
  deleteStaffAccount,
  fetchInventory,
  fetchStaffAccounts,
  restockItem,
  updateStaffAccount,
} from '../api'

const blankStaffForm = {
  name: '',
  telephone: '',
  password: '',
}

function StaffDashboard() {
  const [inventory, setInventory] = useState([])
  const [staffAccounts, setStaffAccounts] = useState([])
  const [restockName, setRestockName] = useState('')
  const [restockAmount, setRestockAmount] = useState(0)
  const [newStaff, setNewStaff] = useState(blankStaffForm)
  const [editingId, setEditingId] = useState('')
  const [editForm, setEditForm] = useState(blankStaffForm)
  const [inventoryMsg, setInventoryMsg] = useState(null)
  const [staffMsg, setStaffMsg] = useState(null)

  const loadInventory = () => {
    fetchInventory().then(data => setInventory(data.items || []))
  }

  const loadStaffAccounts = () => {
    fetchStaffAccounts().then(data => setStaffAccounts(data.items || []))
  }

  useEffect(() => {
    loadInventory()
    loadStaffAccounts()
  }, [])

  const flashMessage = (setter, value) => {
    setter(value)
    window.setTimeout(() => setter(null), 3000)
  }

  const handleRestock = async () => {
    if (!restockName || restockAmount <= 0) return
    const result = await restockItem(restockName, restockAmount)
    flashMessage(setInventoryMsg, result)
    if (result.success) {
      loadInventory()
      setRestockName('')
      setRestockAmount(0)
    }
  }

  const handleCreateStaff = async (e) => {
    e.preventDefault()
    const result = await createStaffAccount(newStaff)
    flashMessage(setStaffMsg, result)
    if (result.success) {
      setNewStaff(blankStaffForm)
      loadStaffAccounts()
    }
  }

  const startEdit = (staff) => {
    setEditingId(staff.staff_id)
    setEditForm({
      name: staff.name,
      telephone: staff.telephone,
      password: staff.password,
    })
  }

  const cancelEdit = () => {
    setEditingId('')
    setEditForm(blankStaffForm)
  }

  const handleUpdateStaff = async (staffId) => {
    const result = await updateStaffAccount(staffId, editForm)
    flashMessage(setStaffMsg, result)
    if (result.success) {
      cancelEdit()
      loadStaffAccounts()
    }
  }

  const handleDeleteStaff = async (staffId, staffName) => {
    const confirmed = window.confirm(`Delete staff account for ${staffName}?`)
    if (!confirmed) return

    const result = await deleteStaffAccount(staffId)
    flashMessage(setStaffMsg, result)
    if (result.success) {
      if (editingId === staffId) {
        cancelEdit()
      }
      loadStaffAccounts()
    }
  }

  return (
    <div className="page">
      <div className="staff-header">
        <div>
          <h2>Staff Dashboard</h2>
          <p className="staff-subtitle">
            Manage live inventory and maintain staff login accounts from one place.
          </p>
        </div>
      </div>

      <div className="staff-grid">
        <section className="staff-panel">
          <div className="staff-panel-title">
            <h3>Inventory Management</h3>
            <p>View stock levels and restock menu items used by the cafe app.</p>
          </div>

          {inventoryMsg && (
            <div className={`message ${inventoryMsg.success ? 'success' : 'error'}`}>
              {inventoryMsg.message}
            </div>
          )}

          <div className="restock-form">
            <div className="field">
              <label>Item Name</label>
              <select
                value={restockName}
                onChange={(e) => setRestockName(e.target.value)}
                className="staff-select"
              >
                <option value="">Select item...</option>
                {inventory.map(item => (
                  <option key={item.name} value={item.name}>{item.name}</option>
                ))}
              </select>
            </div>
            <div className="field">
              <label>Amount</label>
              <input
                type="number"
                min="0"
                value={restockAmount}
                onChange={(e) => setRestockAmount(Math.max(0, parseInt(e.target.value) || 0))}
                onFocus={(e) => e.target.select()}
              />
            </div>
            <button className="btn-success" onClick={handleRestock}>
              Restock
            </button>
          </div>

          <table className="inventory-table">
            <thead>
              <tr>
                <th>Item Name</th>
                <th>Stock</th>
              </tr>
            </thead>
            <tbody>
              {inventory.map(item => (
                <tr key={item.name}>
                  <td>{item.name}</td>
                  <td
                    style={{
                      color: item.quantity <= 5 ? '#d9534f' : 'inherit',
                      fontWeight: item.quantity <= 5 ? 700 : 400,
                    }}
                  >
                    {item.quantity}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="staff-panel">
          <div className="staff-panel-title">
            <h3>Staff Account Management</h3>
            <p>Add, update, and remove staff login accounts used by the terminal and frontend apps.</p>
          </div>

          {staffMsg && (
            <div className={`message ${staffMsg.success ? 'success' : 'error'}`}>
              {staffMsg.message}
            </div>
          )}

          <form className="staff-form-card" onSubmit={handleCreateStaff}>
            <div className="staff-form-header">
              <h4>Create New Staff Account</h4>
            </div>
            <div className="staff-form-grid">
              <input
                type="text"
                value={newStaff.name}
                onChange={(e) => setNewStaff({ ...newStaff, name: e.target.value })}
                placeholder="Staff name"
              />
              <input
                type="text"
                value={newStaff.telephone}
                onChange={(e) => setNewStaff({ ...newStaff, telephone: e.target.value })}
                placeholder="Telephone number"
              />
              <input
                type="text"
                value={newStaff.password}
                onChange={(e) => setNewStaff({ ...newStaff, password: e.target.value })}
                placeholder="Password"
              />
              <button type="submit" className="btn-primary">Create Account</button>
            </div>
          </form>

          <table className="inventory-table staff-table">
            <thead>
              <tr>
                <th>Staff ID</th>
                <th>Name</th>
                <th>Telephone</th>
                <th>Password</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {staffAccounts.map(staff => {
                const isEditing = editingId === staff.staff_id
                return (
                  <tr key={staff.staff_id}>
                    <td>{staff.staff_id}</td>
                    <td>
                      {isEditing ? (
                        <input
                          type="text"
                          value={editForm.name}
                          onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                        />
                      ) : (
                        staff.name
                      )}
                    </td>
                    <td>
                      {isEditing ? (
                        <input
                          type="text"
                          value={editForm.telephone}
                          onChange={(e) => setEditForm({ ...editForm, telephone: e.target.value })}
                        />
                      ) : (
                        staff.telephone
                      )}
                    </td>
                    <td>
                      {isEditing ? (
                        <input
                          type="text"
                          value={editForm.password}
                          onChange={(e) => setEditForm({ ...editForm, password: e.target.value })}
                        />
                      ) : (
                        staff.password
                      )}
                    </td>
                    <td>
                      <div className="table-actions">
                        {isEditing ? (
                          <>
                            <button
                              type="button"
                              className="btn-success btn-small"
                              onClick={() => handleUpdateStaff(staff.staff_id)}
                            >
                              Save
                            </button>
                            <button
                              type="button"
                              className="btn-secondary btn-small"
                              onClick={cancelEdit}
                            >
                              Cancel
                            </button>
                          </>
                        ) : (
                          <>
                            <button
                              type="button"
                              className="btn-primary btn-small"
                              onClick={() => startEdit(staff)}
                            >
                              Edit
                            </button>
                            <button
                              type="button"
                              className="btn-danger btn-small"
                              onClick={() => handleDeleteStaff(staff.staff_id, staff.name)}
                            >
                              Delete
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </section>
      </div>
    </div>
  )
}

export default StaffDashboard
