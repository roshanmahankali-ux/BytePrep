import { useState } from 'react'
import { useAuth, AuthProvider } from './context/AuthContext'
import FlashcardDeck from './components/FlashcardDeck'
import LoginModal from './components/LoginModal'
import AdminPanel from './components/AdminPanel'
import ProfileModal from './components/ProfileModal'
import './App.css'

// Inner component — has access to AuthContext
function AppContent() {
  const { user, loading, logout } = useAuth()
  const [showAdmin, setShowAdmin] = useState(false)
  const [showProfile, setShowProfile] = useState(false)

  if (loading) {
    return (
      <div className="loading-state">
        <div className="spinner" />
        <p>Loading...</p>
      </div>
    )
  }

  // Not logged in — show login screen
  if (!user) {
    return <LoginModal />
  }

  return (
    <div className="app">
      <svg width="0" height="0" style={{ position: 'absolute' }}>
        <defs>
          <linearGradient id="candyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#ec4899" />
            <stop offset="100%" stopColor="#8b5cf6" />
          </linearGradient>
        </defs>
      </svg>

      <header className="app-header">
        <div className="header-top">
          <h1>⚡ System Design Flashcards</h1>
          <div className="header-actions">
            <button className="welcome-text" onClick={() => setShowProfile(true)}>
            👋 {user.username}
            </button>
            {user.is_admin && (
              <button className="admin-btn" onClick={() => setShowAdmin(true)}>
                Admin
              </button>
            )}
            <button className="logout-btn" onClick={logout}>Log out</button>
          </div>
        </div>
        <p>Master system design concepts one card at a time</p>
      </header>

      <main>
        <FlashcardDeck />
      </main>
      {showAdmin && <AdminPanel onClose={() => setShowAdmin(false)} />} 
        {showProfile && <ProfileModal onClose={() => setShowProfile(false)} />}
    </div>
  )
}

// Outer component — provides auth context to everything
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App