import { Link, useLocation } from 'react-router-dom'

export default function Navbar({ user, onLogout }) {
  const { pathname } = useLocation()

  return (
    <nav className="bg-white/80 backdrop-blur-lg border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2.5">
          <span className="text-2xl">💼</span>
          <span className="text-xl font-bold gradient-text">NUSHire</span>
        </Link>

        <div className="flex items-center gap-1">
          <Link to="/"
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
              pathname === '/' ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:text-blue-600 hover:bg-gray-50'
            }`}>
            Browse Jobs
          </Link>

          {user ? (
            <>
              <Link to="/profile"
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                  pathname === '/profile' ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:text-blue-600 hover:bg-gray-50'
                }`}>
                Profile
              </Link>
              <div className="h-6 w-px bg-gray-200 mx-2" />
              <span className="text-sm text-gray-400 mr-2">{user.username}</span>
              <button onClick={onLogout}
                className="btn-secondary text-sm !py-1.5 !px-3">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login"
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                  pathname === '/login' ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:text-blue-600 hover:bg-gray-50'
                }`}>
                Login
              </Link>
              <Link to="/signup" className="btn-primary text-sm !py-1.5 !px-4 ml-1">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
