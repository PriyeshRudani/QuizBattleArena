import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function Navbar() {
  const navigate = useNavigate();
  const { user, logout, isAdmin } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white/10 backdrop-blur-lg border-b border-white/20">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center space-x-2">
            <div className="text-3xl">🎮</div>
            <span className="text-2xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">
              Quiz Battle Arena
            </span>
          </Link>

          <div className="flex items-center space-x-6">
            {user ? (
              <>
                {isAdmin() ? (
                  // Admin Navigation
                  <>
                    <Link to="/admin" className="hover:text-primary-400 transition-colors">
                      🛠️ Admin Dashboard
                    </Link>
                  </>
                ) : (
                  // User Navigation
                  <>
                    <Link to="/leaderboard" className="hover:text-primary-400 transition-colors">
                      🏆 Leaderboard
                    </Link>
                    <Link to="/battle" className="hover:text-primary-400 transition-colors">
                      ⚔️ Battle
                    </Link>
                  </>
                )}
                <div className="flex items-center space-x-4 bg-white/10 rounded-full px-4 py-2 border border-white/20">
                  <span className="text-sm font-semibold">{user.username}</span>
                  {!isAdmin() && (
                    <span className="text-accent-400 font-bold">{user.total_points || 0} pts</span>
                  )}
                  <span className={`text-xs px-2 py-1 rounded ${
                    isAdmin() ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'
                  }`}>
                    {isAdmin() ? '🛠️ Admin' : '🎮 Player'}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  className="btn-secondary"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn-secondary">
                  Login
                </Link>
                <Link to="/register" className="btn-primary">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
