import React, { useState, useEffect } from 'react';
import { leaderboardAPI } from '../api';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [period, setPeriod] = useState('overall');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();
  }, [period]);

  const fetchLeaderboard = async () => {
    setLoading(true);
    try {
      const data = await leaderboardAPI.get(period);
      setLeaderboard(data.leaderboard);
    } catch (error) {
      console.error('Failed to fetch leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRankEmoji = (index) => {
    if (index === 0) return '🥇';
    if (index === 1) return '🥈';
    if (index === 2) return '🥉';
    return `#${index + 1}`;
  };

  const getAvatarColor = (index) => {
    const colors = [
      'from-yellow-400 to-orange-500',
      'from-gray-300 to-gray-500',
      'from-orange-400 to-yellow-700',
      'from-primary-400 to-primary-600',
      'from-secondary-400 to-secondary-600',
      'from-accent-400 to-accent-600',
    ];
    return colors[index % colors.length];
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-5xl font-bold mb-4">🏆 Leaderboard</h1>
          <p className="text-xl text-gray-300">Top performers in the arena</p>
        </div>

        <div className="flex justify-center space-x-4 mb-8">
          {['overall', 'weekly', 'daily'].map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                period === p
                  ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white'
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              }`}
            >
              {p.charAt(0).toUpperCase() + p.slice(1)}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="text-4xl animate-bounce">⏳</div>
          </div>
        ) : (
          <div className="space-y-4">
            {leaderboard.map((user, index) => (
              <div
                key={user.id}
                className="card animate-fade-in"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <div className="flex items-center space-x-4">
                  <div className="text-3xl font-bold min-w-[60px] text-center">
                    {getRankEmoji(index)}
                  </div>

                  <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${getAvatarColor(index)} flex items-center justify-center text-2xl font-bold shadow-lg`}>
                    {user.avatar_url ? (
                      <img src={user.avatar_url} alt={user.username} className="w-full h-full rounded-full object-cover" />
                    ) : (
                      user.username.charAt(0).toUpperCase()
                    )}
                  </div>

                  <div className="flex-1">
                    <h3 className="text-xl font-bold">{user.username}</h3>
                    <div className="flex items-center space-x-2 mt-1">
                      {user.badges && user.badges.length > 0 && (
                        <div className="flex space-x-1">
                          {user.badges.slice(0, 3).map((badge, i) => (
                            <span key={i} className="text-xs">🏅</span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-3xl font-bold text-accent-400">
                      {user.total_points}
                    </div>
                    <div className="text-sm text-gray-400">points</div>
                  </div>
                </div>
              </div>
            ))}

            {leaderboard.length === 0 && (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🤷</div>
                <p className="text-gray-400 text-lg">No data available for this period</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Leaderboard;
