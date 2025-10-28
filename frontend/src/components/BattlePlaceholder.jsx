import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

function BattlePlaceholder() {
  const { user } = useAuth();
  const [searching, setSearching] = useState(false);

  const handleStartBattle = () => {
    setSearching(true);
    setTimeout(() => setSearching(false), 3000);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-5xl font-bold mb-4">⚔️ Battle Arena</h1>
          <p className="text-xl text-gray-300">Challenge other coders in real-time battles</p>
        </div>

        <div className="card mb-8">
          <div className="text-center">
            <div className="text-6xl mb-4">🚧</div>
            <h2 className="text-3xl font-bold mb-2">Coming Soon!</h2>
            <p className="text-gray-300 mb-6">
              Real-time multiplayer battles are currently in development. This feature will allow you to:
            </p>
            
            <div className="grid md:grid-cols-2 gap-4 text-left mb-8">
              <div className="bg-white/5 p-4 rounded-lg">
                <div className="text-2xl mb-2">🎯</div>
                <h3 className="font-bold mb-1">Challenge Friends</h3>
                <p className="text-sm text-gray-400">Send direct challenges to your friends</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg">
                <div className="text-2xl mb-2">⚡</div>
                <h3 className="font-bold mb-1">Quick Match</h3>
                <p className="text-sm text-gray-400">Get matched with random opponents</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg">
                <div className="text-2xl mb-2">🏆</div>
                <h3 className="font-bold mb-1">Ranked Battles</h3>
                <p className="text-sm text-gray-400">Climb the competitive ladder</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg">
                <div className="text-2xl mb-2">💬</div>
                <h3 className="font-bold mb-1">Live Chat</h3>
                <p className="text-sm text-gray-400">Chat with opponents during battles</p>
              </div>
            </div>
          </div>
        </div>

        <div className="card bg-gradient-to-br from-purple-900/30 to-blue-900/30 border-purple-500/30">
          <h3 className="text-2xl font-bold mb-4">Battle Preview</h3>
          <p className="text-gray-300 mb-6">Here's what a battle will look like:</p>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white/10 backdrop-blur rounded-lg p-4 border-2 border-primary-500/50">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-xl font-bold">
                  {user?.username?.charAt(0).toUpperCase() || 'Y'}
                </div>
                <div>
                  <div className="font-bold">{user?.username || 'You'}</div>
                  <div className="text-sm text-gray-400">{user?.total_points || 0} pts</div>
                </div>
              </div>
              <div className="progress-bar mb-2">
                <div className="progress-fill" style={{ width: '65%' }}></div>
              </div>
              <div className="text-sm text-gray-400">3/5 questions answered</div>
            </div>

            <div className="bg-white/10 backdrop-blur rounded-lg p-4 border-2 border-secondary-500/50">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-secondary-400 to-secondary-600 flex items-center justify-center text-xl font-bold">
                  O
                </div>
                <div>
                  <div className="font-bold">Opponent</div>
                  <div className="text-sm text-gray-400">1200 pts</div>
                </div>
              </div>
              <div className="progress-bar mb-2">
                <div className="progress-fill bg-gradient-to-r from-secondary-500 to-red-500" style={{ width: '45%' }}></div>
              </div>
              <div className="text-sm text-gray-400">2/5 questions answered</div>
            </div>
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={handleStartBattle}
              disabled={searching}
              className={`btn-primary ${searching ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {searching ? (
                <>
                  <span className="animate-pulse">🔍 Finding opponent...</span>
                </>
              ) : (
                '⚔️ Start Battle (Demo)'
              )}
            </button>
            {searching && (
              <p className="text-sm text-gray-400 mt-2">
                This is a preview - real battles coming soon with WebSocket support!
              </p>
            )}
          </div>
        </div>

        <div className="mt-8 text-center text-gray-400 text-sm">
          <p>💡 This feature will be enabled after migration to production with Django Channels and Redis</p>
        </div>
      </div>
    </div>
  );
}

export default BattlePlaceholder;
