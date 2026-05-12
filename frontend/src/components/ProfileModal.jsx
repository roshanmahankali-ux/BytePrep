import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import axios from 'axios'

const BASE_URL = 'http://localhost:8000/api'

export default function ProfileModal({ onClose }) {
  const { user, logout, setUser } = useAuth()

  const [username, setUsername] = useState(user.username)
  const [email, setEmail] = useState(user.email)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)
  const [confirmDelete, setConfirmDelete] = useState(false)

  async function handleSave(e) {
    e.preventDefault()
    setError(null)
    setSuccess(null)
    setSaving(true)
    try {
      const res = await axios.put(`${BASE_URL}/auth/me`, { username, email })
      setUser(res.data)          // update global auth state
      setSuccess('Profile updated!')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update profile.')
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete() {
    try {
      await axios.delete(`${BASE_URL}/auth/me`)
      logout()                   // clears token + user, sends back to login
    } catch (err) {
      setError('Failed to delete account.')
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="profile-modal" onClick={e => e.stopPropagation()}>

        <div className="profile-header">
          <h2>👤 My Profile</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <form className="profile-form" onSubmit={handleSave}>
          <label>
            Username
            <input
              value={username}
              onChange={e => setUsername(e.target.value)}
              minLength={2}
              required
            />
          </label>

          <label>
            Email
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
          </label>

          {error   && <p className="profile-error">{error}</p>}
          {success && <p className="profile-success">{success}</p>}

          <button type="submit" className="save-btn" disabled={saving}>
            {saving ? 'Saving…' : 'Save Changes'}
          </button>
        </form>

        <div className="danger-zone">
          {!confirmDelete ? (
            <button className="delete-account-btn" onClick={() => setConfirmDelete(true)}>
              Delete My Account
            </button>
          ) : (
            <div className="confirm-delete">
              <p>This permanently deletes your account and all your history. Are you sure?</p>
              <div className="confirm-actions">
                <button className="confirm-yes" onClick={handleDelete}>Yes, delete it</button>
                <button className="confirm-no" onClick={() => setConfirmDelete(false)}>Cancel</button>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  )
}