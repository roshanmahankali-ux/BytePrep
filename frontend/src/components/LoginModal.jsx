import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import RegisterModal from './RegisterModal'

const LoginModal = () => {
  const { login } = useAuth()
  const [showRegister, setShowRegister] = useState(false)
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.email || !form.password) {
      setError('Please fill in all fields')
      return
    }
    try {
      setLoading(true)
      setError('')
      await login(form.email, form.password)
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  if (showRegister) return <RegisterModal onBack={() => setShowRegister(false)} />

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <h1>⚡ System Design Flashcards</h1>
          <p>Welcome back! Log in to continue studying.</p>
        </div>

        {error && <p className="form-error">{error}</p>}

        <form onSubmit={handleSubmit}>
          <label>Email
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="you@example.com"
            />
          </label>

          <label>Password
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Your password"
            />
          </label>

          <button
            type="submit"
            className="submit-btn full-width"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Log In'}
          </button>
        </form>

        <p className="auth-switch">
          Don't have an account?{' '}
          <button
            className="link-btn"
            onClick={() => setShowRegister(true)}
          >
            Sign up
          </button>
        </p>
      </div>
    </div>
  )
}

export default LoginModal