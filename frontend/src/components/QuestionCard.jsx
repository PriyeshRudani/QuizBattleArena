import React from 'react';

function QuestionCard({ question, onSelect }) {
  const getDifficultyBadge = (difficulty) => {
    const badges = {
      EASY: 'badge-easy',
      MEDIUM: 'badge-medium',
      HARD: 'badge-hard',
    };
    return badges[difficulty] || 'badge-easy';
  };

  const getTypeBadge = (type) => {
    const icons = {
      MCQ: '✅',
      CODE: '💻',
      QUICK: '⚡',
    };
    return icons[type] || '📝';
  };

  return (
    <div className="card cursor-pointer" onClick={() => onSelect(question)}>
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-semibold flex-1">{question.title}</h3>
        <div className="flex items-center space-x-2">
          <span className="text-2xl">{getTypeBadge(question.question_type)}</span>
          <span className={`badge ${getDifficultyBadge(question.difficulty)}`}>
            {question.difficulty}
          </span>
        </div>
      </div>
      
      <p className="text-gray-300 text-sm mb-4 line-clamp-2">{question.question_text}</p>
      
      <div className="flex justify-between items-center text-sm">
        <span className="text-gray-400">{question.category_name}</span>
        <span className="text-accent-400 font-bold">{question.points} pts</span>
      </div>
    </div>
  );
}

export default QuestionCard;
