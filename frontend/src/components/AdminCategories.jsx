import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function AdminCategories() {
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`${API_BASE_URL}/admin/categories/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Handle both paginated and non-paginated responses
      const data = response.data.results || response.data;
      setCategories(Array.isArray(data) ? data : []);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
      setCategories([]);
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure? This will also delete all questions in this category!')) return;

    try {
      const token = localStorage.getItem('access_token');
      await axios.delete(`${API_BASE_URL}/admin/categories/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCategories(categories.filter(c => c.id !== id));
      alert('Category deleted successfully');
    } catch (error) {
      console.error('Failed to delete category:', error);
      alert('Failed to delete category');
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
          <h1 className="text-3xl font-bold mb-2">📁 Category Management</h1>
          <p className="text-gray-400">Manage quiz categories</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {categories.map((category) => (
          <div key={category.id} className="card">
            <h3 className="text-xl font-bold mb-2">{category.name}</h3>
            <p className="text-gray-400 text-sm mb-4">{category.description}</p>
            <div className="flex items-center justify-between">
              <span className="text-primary-400 font-bold">
                {category.question_count} questions
              </span>
              <button
                onClick={() => handleDelete(category.id)}
                className="px-3 py-1 bg-red-500 hover:bg-red-600 rounded text-sm"
              >
                🗑️ Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      <button
        onClick={() => navigate('/admin')}
        className="btn-secondary mt-6"
      >
        ← Back to Dashboard
      </button>
    </div>
  );
}

export default AdminCategories;
