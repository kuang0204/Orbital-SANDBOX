import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'

export default function LoginPage({ onAuth }) {
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      const data = await api.login(form)
      onAuth(data)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <span className="text-5xl">💼</span>
          <h1 className="text-2xl font-bold gradient-text mt-3">Welcome Back</h1>
          <p className="text-gray-500 text-sm mt-1">Sign in to continue to NUSHire</p>
        </div>

        <form onSubmit={handleSubmit} className="card p-8 space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Username</label>
            <input type="text" value={form.username} onChange={e => setForm({ ...form, username: e.target.value })}
              className="input-field" placeholder="Enter your username" required />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Password</label>
            <input type="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })}
              className="input-field" placeholder="Enter your password" required />
          </div>

          {error && <p className="text-red-600 text-sm bg-red-50 rounded-lg p-3">{error}</p>}

          <button type="submit" className="btn-primary w-full">Sign In</button>

          <p className="text-sm text-center text-gray-500">
            Don't have an account? <Link to="/signup" className="text-blue-600 font-medium hover:underline">Sign up</Link>
          </p>

          <div className="text-xs text-gray-400 text-center border-t border-gray-100 pt-4 mt-2">
            <p className="mb-1 font-medium">Demo Accounts</p>
            <p><span className="font-mono">alice</span> / <span className="font-mono">password123</span></p>
            <p><span className="font-mono">bob</span> / <span className="font-mono">password123</span></p>
          </div>
        </form>
      </div>
    </div>
  )
}
