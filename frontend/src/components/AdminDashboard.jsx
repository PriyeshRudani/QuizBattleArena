import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function AdminDashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`${API_BASE_URL}/admin/dashboard/stats/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch dashboard stats:', error);
      setLoading(false);
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
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">🛠️ Admin Dashboard</h1>
        <p className="text-gray-400">Platform management and analytics</p>
      </div>

      {/* Navigation Tabs */}
      <div className="flex space-x-2 mb-6 overflow-x-auto">
        <button
          onClick={() => setActiveTab('overview')}
          className={`px-6 py-3 rounded-lg font-semibold transition-all ${
            activeTab === 'overview'
              ? 'bg-primary-500 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          }`}
        >
          📊 Overview
        </button>
        <button
          onClick={() => setActiveTab('questions')}
          className={`px-6 py-3 rounded-lg font-semibold transition-all ${
            activeTab === 'questions'
              ? 'bg-primary-500 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          }`}
        >
          ❓ Questions
        </button>
        <button
          onClick={() => setActiveTab('categories')}
          className={`px-6 py-3 rounded-lg font-semibold transition-all ${
            activeTab === 'categories'
              ? 'bg-primary-500 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          }`}
        >
          📁 Categories
        </button>
        <button
          onClick={() => setActiveTab('users')}
          className={`px-6 py-3 rounded-lg font-semibold transition-all ${
            activeTab === 'users'
              ? 'bg-primary-500 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          }`}
        >
          👥 Users
        </button>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && stats && (
        <div>
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="card text-center">
              <div className="text-5xl mb-3">👥</div>
              <div className="text-3xl font-bold text-primary-400">{stats.overview.total_users}</div>
              <div className="text-gray-400">Total Users</div>
            </div>
            <div className="card text-center">
              <div className="text-5xl mb-3">❓</div>
              <div className="text-3xl font-bold text-accent-400">{stats.overview.total_questions}</div>
              <div className="text-gray-400">Questions</div>
            </div>
            <div className="card text-center">
              <div className="text-5xl mb-3">📁</div>
              <div className="text-3xl font-bold text-green-400">{stats.overview.total_categories}</div>
              <div className="text-gray-400">Categories</div>
            </div>
            <div className="card text-center">
              <div className="text-5xl mb-3">🎯</div>
              <div className="text-3xl font-bold text-yellow-400">{stats.overview.total_quiz_attempts}</div>
              <div className="text-gray-400">Quiz Attempts</div>
            </div>
          </div>

          {/* Top Performers */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="text-xl font-bold mb-4">🏆 Top Performers</h3>
              <div className="space-y-3">
                {stats.top_performers && stats.top_performers.map((user, index) => (
                  <div key={index} className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="text-2xl">#{index + 1}</div>
                      <div className="font-semibold">{user.username}</div>
                    </div>
                    <div className="text-accent-400 font-bold">{user.points} pts</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="card">
              <h3 className="text-xl font-bold mb-4">🆕 Recent Users</h3>
              <div className="space-y-3">
                {stats.recent_users && stats.recent_users.map((user, index) => (
                  <div key={index} className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                    <div className="font-semibold">{user.username}</div>
                    <div className="text-sm text-gray-400">
                      {new Date(user.date_joined).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Questions Tab */}
      {activeTab === 'questions' && (
        <div className="card">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-2xl font-bold">❓ Question Management</h3>
            <button
              onClick={() => navigate('/admin/questions/create')}
              className="btn-primary"
            >
              ➕ Add Question
            </button>
          </div>
          <button
            onClick={() => navigate('/admin/questions')}
            className="btn-secondary w-full"
          >
            View All Questions →
          </button>
        </div>
      )}

      {/* Categories Tab */}
      {activeTab === 'categories' && (
        <div className="card">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-2xl font-bold">📁 Category Management</h3>
            <button
              onClick={() => navigate('/admin/categories/create')}
              className="btn-primary"
            >
              ➕ Add Category
            </button>
          </div>
          <button
            onClick={() => navigate('/admin/categories')}
            className="btn-secondary w-full"
          >
            View All Categories →
          </button>
        </div>
      )}

      {/* Users Tab */}
      {activeTab === 'users' && (
        <div className="card">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-2xl font-bold">👥 User Management</h3>
          </div>
          <button
            onClick={() => navigate('/admin/users')}
            className="btn-secondary w-full"
          >
            View All Users →
          </button>
        </div>
      )}
    </div>
  );
}

export default AdminDashboard;
