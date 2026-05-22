import { useState, useEffect } from 'react'
import axios from 'axios'

const BASE_URL = 'http://localhost:8000/api'

export default function AdminPanel({ onClose, asPage = false }) {
  const [users, setUsers] = useState([])
  const [selectedUser, setSelectedUser] = useState(null)
  const [reviewHistory, setReviewHistory] = useState([])
  const [view, setView] = useState('users')
  const [loadingUsers, setLoadingUsers] = useState(true)
  const [loadingHistory, setLoadingHistory] = useState(false)
  const [error, setError] = useState(null)
  const [userSearch, setUserSearch] = useState('')

  useEffect(() => { fetchUsers() }, [])

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

  async function openHistory(userId, username) {
    try {
      setLoadingHistory(true)
      setSelectedUser(username)
      setView('history')
      const res = await axios.get(`${BASE_URL}/admin/users/${userId}/history`)
      setReviewHistory(res.data.history ?? [])
    } catch (err) {
      setError('Failed to load history for this user.')
    } finally {
      setLoadingHistory(false)
    }
  }

  function goBack() {
    setView('users')
    setSelectedUser(null)
    setReviewHistory([])
    setUserSearch('')
  }

  async function toggleAdmin(userId, currentIsAdmin) {
    try {
      await axios.put(`${BASE_URL}/admin/users/${userId}`, { is_admin: !currentIsAdmin })
      setUsers(users.map(u => u.id === userId ? { ...u, is_admin: !currentIsAdmin } : u))
    } catch (err) {
      setError('Failed to update admin status.')
    }
  }

  async function deleteUser(userId, username) {
    if (!confirm(`Delete user "${username}"? This also deletes their history.`)) return
    try {
      await axios.delete(`${BASE_URL}/admin/users/${userId}`)
      setUsers(users.filter(u => u.id !== userId))
    } catch (err) {
      setError('Failed to delete user.')
    }
  }

  const filteredUsers = users.filter(u => {
  if (!userSearch.trim()) return true
  const q = userSearch.toLowerCase()
  return u.username.toLowerCase().includes(q) || u.email.toLowerCase().includes(q)
})

  const content = (
    <div className={asPage ? 'admin-page' : 'admin-panel'} onClick={e => e.stopPropagation()}>

      <div className="admin-header">
        {view === 'history' ? (
          <button className="back-btn" onClick={goBack}>← Back</button>
        ) : (
          <h2>Admin Dashboard</h2>
        )}
        {view === 'history' && <h2>{selectedUser}'s History</h2>}
        {!asPage && <button className="close-btn" onClick={onClose}>✕</button>}
      </div>

      {error && <div className="admin-error">{error}</div>}

      {/* ── Users view ── */}
      {view === 'users' && (
        <div className="admin-view">
          <input
            className="search-bar admin-search"
            type="text"
            placeholder="Search by name or email..."
            value={userSearch}
            onChange={e => setUserSearch(e.target.value)}
          />
          <h3>All Users ({users.length})</h3>
          {loadingUsers ? (
            <p className="admin-loading">Loading users…</p>
          ) : (
            <>
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
                {filteredUsers.map(u => (
                  <tr key={u.id}>
                    <td>
                      <button className="user-link" onClick={() => openHistory(u.id, u.username)}>
                        {u.username}
                      </button>
                    </td>
                    <td><span className="email-text">{u.email}</span></td>
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
                      <button className="delete-btn" onClick={() => deleteUser(u.id, u.username)} title="Delete User" >⌫</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="admin-hint">Click a username to view the User's history</p>
            </>
          )}
        </div>
      )}

      {/* ── History view ── */}
      {view === 'history' && (
        <div className="admin-view">
          {loadingHistory ? (
            <p className="admin-loading">Loading history…</p>
          ) : reviewHistory.length === 0 ? (
            <p className="admin-empty">No cards reviewed yet.</p>
          ) : (
            <>
              <h3>{reviewHistory.length} cards reviewed</h3>
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
            </>
          )}
        </div>
      )}

    </div>
  )

  if (asPage) return content
  return (
    <div className="admin-overlay" onClick={onClose}>
      {content}
    </div>
  )
}