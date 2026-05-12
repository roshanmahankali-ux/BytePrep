import { useState, useEffect } from 'react'
import axios from 'axios'

const BASE_URL = 'http://localhost:8000/api'

export default function AdminPanel({ onClose }) {
  const [users, setUsers] = useState([])
  const [selectedUser, setSelectedUser] = useState(null)
  const [reviewHistory, setReviewHistory] = useState([])
  const [loadingUsers, setLoadingUsers] = useState(true)
  const [loadingHistory, setLoadingHistory] = useState(false)
  const [error, setError] = useState(null)

  // Fetch all users when panel opens
  useEffect(() => {
    fetchUsers()
  }, [])

  async function fetchUsers() {
    try {
      setLoadingUsers(true)
      const res = await axios.get(`${BASE_URL}/admin/users`)
      setUsers(res.data)
    } catch (err) {
      setError('Failed to load users. Are you logged in as admin?')
    } finally {
      setLoadingUsers(false)
    }
  }

  async function fetchHistory(userId, username) {
    try {
      setLoadingHistory(true)
      setSelectedUser(username)
      const res = await axios.get(`${BASE_URL}/admin/users/${userId}/history`)
      setReviewHistory(res.data.history ?? [])
    } catch (err) {
      setError('Failed to load history for this user.')
    } finally {
      setLoadingHistory(false)
    }
  }

  async function toggleAdmin(userId, currentIsAdmin) {
    try {
      await axios.put(`${BASE_URL}/admin/users/${userId}`, {
        is_admin: !currentIsAdmin
      })
      setUsers(users.map(u =>
        u.id === userId ? { ...u, is_admin: !currentIsAdmin } : u
      ))
    } catch (err) {
      setError('Failed to update admin status.')
    }
  }

  async function deleteUser(userId, username) {
    if (!confirm(`Delete user "${username}"? This also deletes their history.`)) return
    try {
      await axios.delete(`${BASE_URL}/admin/users/${userId}`)
      setUsers(users.filter(u => u.id !== userId))
      if (selectedUser === username) {
        setSelectedUser(null)
        setReviewHistory([])
      }
    } catch (err) {
      setError('Failed to delete user.')
    }
  }

  return (
    <div className="admin-overlay" onClick={onClose}>
      <div className="admin-panel" onClick={e => e.stopPropagation()}>
        <div className="admin-header">
          <h2>Admin Panel</h2>
          <button className="close-btn" onClick={onClose} aria-label="Close">✕</button>
        </div>

        {error && <div className="admin-error">{error}</div>}

        <div className="admin-body">
          {/* Left: user list */}
          <div className="admin-users">
            <h3>All Users ({users.length})</h3>
            {loadingUsers ? (
              <p className="admin-loading">Loading users…</p>
            ) : (
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Admin?</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map(u => (
                    <tr
                      key={u.id}
                      className={selectedUser === u.username ? 'selected-row' : ''}
                    >
                      <td>
                        <button
                          className="user-link"
                          onClick={() => fetchHistory(u.id, u.username)}
                        >
                          {u.username}
                        </button>
                      </td>
                      <td>{u.email}</td>
                      <td>
                        <span className={`badge ${u.is_admin ? 'badge-admin' : 'badge-user'}`}>
                          {u.is_admin ? 'Admin' : 'User'}
                        </span>
                      </td>
                      <td className="action-cell">
                    <button
                    className={`text-action-btn ${u.is_admin ? 'remove-admin-btn' : 'add-admin-btn'}`}
                    onClick={() => toggleAdmin(u.id, u.is_admin)}
                    >
                    {u.is_admin
                        ? <><span className="red-x">✕</span> Remove admin</>
                        : '↑ Make admin'}
                    </button>
                        <button
                          className="action-btn delete-btn"
                          onClick={() => deleteUser(u.id, u.username)}
                          title="Delete user"
                        >
                          🗑
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {/* Right: history panel */}
          <div className="admin-history">
            <h3>
              {selectedUser
                ? `${selectedUser}'s Review History (${reviewHistory.length} cards reviewed)`
                : 'Select a user to see history'}
            </h3>
            {loadingHistory ? (
              <p className="admin-loading">Loading history…</p>
            ) : selectedUser && reviewHistory.length === 0 ? (
              <p className="admin-empty">No cards reviewed yet.</p>
            ) : (
              <div className="history-list">
                {reviewHistory.map((entry, i) => (
                  <div key={i} className="history-entry">
                    <div className="history-question">{entry.question}</div>
                    <div className="history-meta">
                      <span className={`difficulty-tag diff-${entry.difficulty?.toLowerCase()}`}>
                        {entry.difficulty}
                      </span>
                      <span className="history-time">
                        {new Date(entry.reviewed_at).toLocaleString()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}