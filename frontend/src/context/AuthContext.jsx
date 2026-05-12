import { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const BASE_URL = 'http://localhost:8000'
const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)        // current logged in user
  const [token, setToken] = useState(null)      // JWT token
  const [loading, setLoading] = useState(true)  // checking token on load

  // On app load — check if there's a saved token
  useEffect(() => {
    const savedToken = localStorage.getItem('token')
    if (savedToken) {
      verifyToken(savedToken)
    } else {
      setLoading(false)
    }
  }, [])

  const verifyToken = async (savedToken) => {
    try {
      // Ask backend "who owns this token?"
      const res = await axios.get(`${BASE_URL}/api/auth/me`, {
        headers: { Authorization: `Bearer ${savedToken}` }
      })
      setUser(res.data)
      setToken(savedToken)
    } catch {
      // Token expired or invalid — clear it
      localStorage.removeItem('token')
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    const res = await axios.post(`${BASE_URL}/api/auth/login`, {
      email,
      password
    })
    const { access_token, user } = res.data
    localStorage.setItem('token', access_token)
    setToken(access_token)
    setUser(user)
    return user
  }

  const register = async (username, email, password) => {
    const res = await axios.post(`${BASE_URL}/api/auth/register`, {
      username,
      email,
      password,
      is_admin: false
    })
    const { access_token, user } = res.data
    localStorage.setItem('token', access_token)
    setToken(access_token)
    setUser(user)
    return user
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  )
}

// Custom hook — any component can call useAuth() to get user/token/login/logout
export const useAuth = () => useContext(AuthContext)