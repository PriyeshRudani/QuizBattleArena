import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { categoryAPI } from '../api';

const categoryIcons = {
  'Programming Fundamentals': '💻',
  'Web Development': '🌐',
  'Database & SQL': '🗄️',
  'Computer Networks': '🔗',
  'Operating Systems': '⚙️',
  'Data Structures & Algorithms': '🧮',
  'Cybersecurity': '🔒',
  'DevOps & Cloud': '☁️',
  'Software Engineering': '🛠️',
  'Tech Trivia & Innovations': '🚀',
};

function Dashboard() {
  const { user, isAdmin } = useAuth();
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect admins to admin dashboard
    if (isAdmin()) {
      navigate('/admin');
      return;
    }
    fetchCategories();
  }, [isAdmin, navigate]);

  const fetchCategories = async () => {
    try {
      const data = await categoryAPI.getAll();
      setCategories(data.results || data);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePlay = (category) => {
    navigate(`/quiz/${category.slug}`, { state: { category } });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-4xl animate-bounce">🎮</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-12 text-center animate-fade-in">
        <h1 className="text-5xl font-bold mb-4">
          Welcome back, <span className="bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">
            {user?.username || 'Challenger'}
          </span>! 👋
        </h1>
        <p className="text-xl text-gray-300">Choose your category and start battling</p>
        
        {user && (
          <div className="mt-6 flex justify-center space-x-8">
            <div className="bg-white/10 backdrop-blur rounded-lg px-6 py-3 border border-white/20">
              <div className="text-3xl font-bold text-accent-400">{user.total_points || 0}</div>
              <div className="text-sm text-gray-400">Total Points</div>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-lg px-6 py-3 border border-white/20">
              <div className="text-3xl font-bold text-primary-400">{user.badges?.length || 0}</div>
              <div className="text-sm text-gray-400">Badges</div>
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {categories.map((category, index) => (
          <div
            key={category.id}
            className="card animate-fade-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="text-6xl mb-4 text-center">
              {categoryIcons[category.name] || '📚'}
            </div>
            
            <h3 className="text-2xl font-bold mb-2 text-center">{category.name}</h3>
            <p className="text-gray-300 text-sm mb-4 text-center">{category.description}</p>
            
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">Questions</span>
                <span className="font-semibold text-primary-300">{category.question_count}</span>
              </div>
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${Math.min((category.question_count / 50) * 100, 100)}%` }}
                ></div>
              </div>
            </div>
            
            <button
              onClick={() => handlePlay(category)}
              className="btn-primary w-full"
            >
              🎯 Play Now
            </button>
          </div>
        ))}
      </div>

      {categories.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-400 text-lg">No categories available yet.</p>
          <p className="text-gray-500 mt-2">Please run the seed command on the backend.</p>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
