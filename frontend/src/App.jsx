import { Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import ProfilePage from './pages/ProfilePage'
import JobListPage from './pages/JobListPage'
import JobDetailPage from './pages/JobDetailPage'
import OutcomeSubmitPage from './pages/OutcomeSubmitPage'
import { api } from './api'

export default function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (localStorage.getItem('token')) {
      api.getProfile()
        .then(() => {
          setUser({ username: localStorage.getItem('username') })
        })
        .catch(() => {
          localStorage.removeItem('token')
          localStorage.removeItem('username')
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  function handleAuth(userData) {
    localStorage.setItem('token', userData.token)
    localStorage.setItem('username', userData.user.username)
    setUser(userData.user)
  }

  function handleLogout() {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    setUser(null)
  }

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="flex flex-col items-center gap-3">
        <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-gray-400 text-sm">Loading...</p>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen">
      <Navbar user={user} onLogout={handleLogout} />
      <main className="max-w-6xl mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<JobListPage user={user} />} />
          <Route path="/login" element={user ? <Navigate to="/" /> : <LoginPage onAuth={handleAuth} />} />
          <Route path="/signup" element={user ? <Navigate to="/" /> : <SignupPage onAuth={handleAuth} />} />
          <Route path="/profile" element={user ? <ProfilePage /> : <Navigate to="/login" />} />
          <Route path="/jobs/:id" element={<JobDetailPage user={user} />} />
          <Route path="/jobs/:id/outcome" element={user ? <OutcomeSubmitPage /> : <Navigate to="/login" />} />
        </Routes>
      </main>
    </div>
  )
}
