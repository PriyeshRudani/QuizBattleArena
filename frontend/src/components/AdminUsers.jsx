import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function AdminUsers() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchUsers();
  }, [filter]);

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const url = filter === 'all'
        ? `${API_BASE_URL}/admin/users/`
        : `${API_BASE_URL}/admin/users/?role=${filter}`;
      
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Handle both paginated and non-paginated responses
      const data = response.data.results || response.data;
      setUsers(Array.isArray(data) ? data : []);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch users:', error);
      setUsers([]);
      setLoading(false);
    }
  };

  const toggleActive = async (userId) => {
    try {
      const token = localStorage.getItem('access_token');
      await axios.patch(
        `${API_BASE_URL}/admin/users/${userId}/toggle_active/`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchUsers();
      alert('User status updated');
    } catch (error) {
      console.error('Failed to toggle user status:', error);
      alert('Failed to update user status');
    }
  };

  const changeRole = async (userId, newRole) => {
    if (!window.confirm(`Change user role to ${newRole}?`)) return;

    try {
      const token = localStorage.getItem('access_token');
      await axios.patch(
        `${API_BASE_URL}/admin/users/${userId}/change_role/`,
        { role: newRole },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchUsers();
      alert('User role updated');
    } catch (error) {
      console.error('Failed to change role:', error);
      alert('Failed to change role');
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-4xl animate-bounce">⏳</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">👥 User Management</h1>
          <p className="text-gray-400">Manage platform users</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex space-x-2 mb-6">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'all' ? 'bg-primary-500' : 'bg-white/10 hover:bg-white/20'
          }`}
        >
          All Users
        </button>
        <button
          onClick={() => setFilter('admin')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'admin' ? 'bg-primary-500' : 'bg-white/10 hover:bg-white/20'
          }`}
        >
          🛠️ Admins
        </button>
        <button
          onClick={() => setFilter('user')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'user' ? 'bg-primary-500' : 'bg-white/10 hover:bg-white/20'
          }`}
        >
          🎮 Players
        </button>
      </div>

      {/* Users List */}
      <div className="space-y-4">
        {users.map((user) => (
          <div key={user.id} className="card">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h3 className="text-xl font-bold">{user.username}</h3>
                  <span className={`badge ${
                    user.role === 'admin' ? 'badge-hard' : 'badge-easy'
                  }`}>
                    {user.role === 'admin' ? '🛠️ Admin' : '🎮 Player'}
                  </span>
                  {!user.is_active && (
                    <span className="badge bg-gray-500">Inactive</span>
                  )}
                </div>
                <div className="flex items-center space-x-4 text-sm text-gray-400">
                  <span>📧 {user.email}</span>
                  {user.total_points !== undefined && (
                    <span>🎯 {user.total_points} pts</span>
                  )}
                  <span>📅 Joined: {new Date(user.date_joined).toLocaleDateString()}</span>
                </div>
              </div>
              <div className="flex space-x-2 ml-4">
                <button
                  onClick={() => toggleActive(user.id)}
                  className={`px-4 py-2 rounded-lg ${
                    user.is_active
                      ? 'bg-yellow-500 hover:bg-yellow-600'
                      : 'bg-green-500 hover:bg-green-600'
                  }`}
                >
                  {user.is_active ? '⏸️ Deactivate' : '✅ Activate'}
                </button>
                <button
                  onClick={() => changeRole(user.id, user.role === 'admin' ? 'user' : 'admin')}
                  className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg"
                >
                  {user.role === 'admin' ? '↓ Make Player' : '↑ Make Admin'}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {users.length === 0 && (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">📭</div>
          <p className="text-gray-400">No users found</p>
        </div>
      )}

      <button
        onClick={() => navigate('/admin')}
        className="btn-secondary mt-6"
      >
        ← Back to Dashboard
      </button>
    </div>
  );
}

export default AdminUsers;
