import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function AdminQuestions() {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`${API_BASE_URL}/admin/questions/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Handle both paginated and non-paginated responses
      const data = response.data.results || response.data;
      setQuestions(Array.isArray(data) ? data : []);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch questions:', error);
      setQuestions([]);
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this question?')) return;

    try {
      const token = localStorage.getItem('access_token');
      await axios.delete(`${API_BASE_URL}/admin/questions/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setQuestions(questions.filter(q => q.id !== id));
      alert('Question deleted successfully');
    } catch (error) {
      console.error('Failed to delete question:', error);
      alert('Failed to delete question');
    }
  };

  const filteredQuestions = filter === 'all'
    ? questions
    : questions.filter(q => q.question_type === filter);

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
          <h1 className="text-3xl font-bold mb-2">❓ Question Management</h1>
          <p className="text-gray-400">Manage quiz questions</p>
        </div>
        <button
          onClick={() => navigate('/admin/questions/create')}
          className="btn-primary"
        >
          ➕ Add Question
        </button>
      </div>

      {/* Filters */}
      <div className="flex space-x-2 mb-6 overflow-x-auto">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'all' ? 'bg-primary-500' : 'bg-white/10 hover:bg-white/20'
          }`}
        >
          All ({questions.length})
        </button>
        <button
          onClick={() => setFilter('MCQ')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'MCQ' ? 'bg-primary-500' : 'bg-white/10 hover:bg-white/20'
          }`}
        >
          ✅ MCQ ({questions.filter(q => q.question_type === 'MCQ').length})
        </button>
        <button
          onClick={() => setFilter('CODE')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'CODE' ? 'bg-primary-500' : 'bg-white/10 hover:bg-white/20'
          }`}
        >
          💻 CODE ({questions.filter(q => q.question_type === 'CODE').length})
        </button>
        <button
          onClick={() => setFilter('QUICK')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'QUICK' ? 'bg-primary-500' : 'bg-white/10 hover:bg-white/20'
          }`}
        >
          ⚡ QUICK ({questions.filter(q => q.question_type === 'QUICK').length})
        </button>
      </div>

      {/* Questions List */}
      <div className="space-y-4">
        {filteredQuestions.map((question) => (
          <div key={question.id} className="card">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <span className="text-2xl">
                    {question.question_type === 'MCQ' ? '✅' :
                     question.question_type === 'CODE' ? '💻' : '⚡'}
                  </span>
                  <h3 className="text-xl font-bold">{question.title}</h3>
                  <span className={`badge ${
                    question.difficulty === 'EASY' ? 'badge-easy' :
                    question.difficulty === 'MEDIUM' ? 'badge-medium' : 'badge-hard'
                  }`}>
                    {question.difficulty}
                  </span>
                </div>
                <p className="text-gray-300 mb-2">{question.question_text.substring(0, 100)}...</p>
                <div className="flex items-center space-x-4 text-sm text-gray-400">
                  <span>📁 {question.category_name}</span>
                  <span>🎯 {question.points} pts</span>
                  <span>🔤 {question.language}</span>
                </div>
              </div>
              <div className="flex space-x-2 ml-4">
                <button
                  onClick={() => navigate(`/admin/questions/edit/${question.id}`)}
                  className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg"
                >
                  ✏️ Edit
                </button>
                <button
                  onClick={() => handleDelete(question.id)}
                  className="px-4 py-2 bg-red-500 hover:bg-red-600 rounded-lg"
                >
                  🗑️ Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredQuestions.length === 0 && (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">📭</div>
          <p className="text-gray-400">No questions found</p>
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

export default AdminQuestions;
