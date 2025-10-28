import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export const ProtectedRoute = ({ children, requireAdmin = false, requireUser = false }) => {
  const { user, loading, isAdmin, isUser } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-6xl animate-bounce">🎮</div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (requireAdmin && !isAdmin()) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card max-w-md text-center">
          <div className="text-6xl mb-4">🚫</div>
          <h2 className="text-2xl font-bold mb-2">Access Denied</h2>
          <p className="text-gray-400 mb-6">
            You need admin privileges to access this page.
          </p>
          <button
            onClick={() => window.history.back()}
            className="btn-primary"
          >
            ← Go Back
          </button>
        </div>
      </div>
    );
  }

  if (requireUser && !isUser()) {
    console.log('Access denied - User check:', { user, isUser: isUser(), isAdmin: isAdmin() }); // Debug
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card max-w-md text-center">
          <div className="text-6xl mb-4">🎮</div>
          <h2 className="text-2xl font-bold mb-2">Players Only</h2>
          <p className="text-gray-400 mb-6">
            This feature is only available for regular users. Admins manage content but don't participate in quizzes.
          </p>
          <p className="text-xs text-gray-500 mb-4">
            Debug: role={user?.role}, is_admin={user?.is_admin ? 'true' : 'false'}
          </p>
          <button
            onClick={() => window.history.back()}
            className="btn-primary"
          >
            ← Go Back
          </button>
        </div>
      </div>
    );
  }

  return children;
};

export default ProtectedRoute;
