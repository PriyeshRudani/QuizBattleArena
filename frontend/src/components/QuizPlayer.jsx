import React, { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { categoryAPI, questionAPI } from '../api';
import confetti from 'canvas-confetti';

function QuizPlayer({ user, onUpdateUser }) {
  const { slug } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [codeAnswer, setCodeAnswer] = useState('');
  const [textAnswer, setTextAnswer] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [timer, setTimer] = useState(0);
  const [timerActive, setTimerActive] = useState(false);

  useEffect(() => {
    fetchQuestions();
  }, [slug]);

  useEffect(() => {
    let interval;
    if (timerActive) {
      interval = setInterval(() => {
        setTimer((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [timerActive]);

  useEffect(() => {
    if (questions.length > 0) {
      setTimerActive(true);
    }
  }, [questions]);

  const fetchQuestions = async () => {
    try {
      const data = await categoryAPI.getQuestions(slug, { limit: 10 });
      setQuestions(data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch questions:', error);
      setLoading(false);
    }
  };

  const triggerConfetti = () => {
    const count = 200;
    const defaults = {
      origin: { y: 0.7 }
    };

    function fire(particleRatio, opts) {
      confetti({
        ...defaults,
        ...opts,
        particleCount: Math.floor(count * particleRatio)
      });
    }

    fire(0.25, {
      spread: 26,
      startVelocity: 55,
    });

    fire(0.2, {
      spread: 60,
    });

    fire(0.35, {
      spread: 100,
      decay: 0.91,
      scalar: 0.8
    });

    fire(0.1, {
      spread: 120,
      startVelocity: 25,
      decay: 0.92,
      scalar: 1.2
    });

    fire(0.1, {
      spread: 120,
      startVelocity: 45,
    });
  };

  const handleSubmit = async () => {
    if (!user) {
      alert('Please login to submit answers');
      return;
    }

    const question = questions[currentIndex];
    setSubmitting(true);
    setTimerActive(false);

    try {
      let payload = { time_taken: timer };

      if (question.question_type === 'MCQ') {
        payload.answer = selectedAnswer;
      } else if (question.question_type === 'CODING') {
        payload.code = codeAnswer;
        payload.language = question.language;
      } else if (question.question_type === 'QUICK') {
        payload.answer = textAnswer.toLowerCase();
      }

      const response = await questionAPI.submitAnswer(question.id, payload);
      setResult(response);

      if (response.correct) {
        triggerConfetti();
      }

      if (onUpdateUser) {
        onUpdateUser({ ...user, total_points: response.total_points });
      }
    } catch (error) {
      console.error('Failed to submit answer:', error);
      alert('Failed to submit answer. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setSelectedAnswer(null);
      setCodeAnswer('');
      setTextAnswer('');
      setResult(null);
      setTimer(0);
      setTimerActive(true);
    } else {
      navigate('/');
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-4xl animate-bounce">⏳</div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card max-w-md text-center">
          <div className="text-6xl mb-4">😔</div>
          <h2 className="text-2xl font-bold mb-2">No Questions Available</h2>
          <p className="text-gray-400 mb-6">This category doesn't have any questions yet.</p>
          <button onClick={() => navigate('/')} className="btn-primary">
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const question = questions[currentIndex];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div className="text-sm text-gray-400">
            Question {currentIndex + 1} of {questions.length}
          </div>
          <div className="flex items-center space-x-4">
            <div className={`text-2xl font-bold ${timer > 60 ? 'text-red-400 timer-pulse' : 'text-primary-400'}`}>
              ⏱️ {formatTime(timer)}
            </div>
            <div className="text-accent-400 font-bold">{question.points} pts</div>
          </div>
        </div>

        <div className="card animate-fade-in">
          <div className="flex justify-between items-start mb-4">
            <h2 className="text-2xl font-bold flex-1">{question.title}</h2>
            <span className={`badge ${
              question.difficulty === 'EASY' ? 'badge-easy' :
              question.difficulty === 'MEDIUM' ? 'badge-medium' : 'badge-hard'
            }`}>
              {question.difficulty}
            </span>
          </div>

          <div className="prose prose-invert max-w-none mb-6">
            <pre className="bg-gray-800/50 p-4 rounded-lg overflow-x-auto whitespace-pre-wrap">
              {question.question_text}
            </pre>
          </div>

          {question.question_type === 'MCQ' && question.options && (
            <div className="space-y-3">
              {question.options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => !result && setSelectedAnswer(index)}
                  disabled={!!result}
                  className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                    selectedAnswer === index
                      ? 'border-primary-500 bg-primary-500/20'
                      : 'border-white/20 bg-white/5 hover:border-white/40'
                  } ${result ? 'cursor-not-allowed' : 'cursor-pointer'}`}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                      selectedAnswer === index ? 'border-primary-500 bg-primary-500' : 'border-white/40'
                    }`}>
                      {selectedAnswer === index && <span className="text-white text-sm">✓</span>}
                    </div>
                    <span>{option}</span>
                  </div>
                </button>
              ))}
            </div>
          )}

          {question.question_type === 'CODING' && (
            <div>
              <label className="block text-sm font-medium mb-2">
                Your Solution ({question.language}):
              </label>
              <textarea
                value={codeAnswer}
                onChange={(e) => setCodeAnswer(e.target.value)}
                disabled={!!result}
                className="w-full h-64 px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-green-400 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Write your code here..."
              />
            </div>
          )}

          {question.question_type === 'QUICK' && (
            <div>
              <label className="block text-sm font-medium mb-2">
                Your Answer (true/false):
              </label>
              <div className="flex space-x-4">
                <button
                  onClick={() => !result && setTextAnswer('true')}
                  disabled={!!result}
                  className={`flex-1 p-4 rounded-lg border-2 transition-all ${
                    textAnswer === 'true'
                      ? 'border-green-500 bg-green-500/20'
                      : 'border-white/20 bg-white/5 hover:border-white/40'
                  }`}
                >
                  ✅ True
                </button>
                <button
                  onClick={() => !result && setTextAnswer('false')}
                  disabled={!!result}
                  className={`flex-1 p-4 rounded-lg border-2 transition-all ${
                    textAnswer === 'false'
                      ? 'border-red-500 bg-red-500/20'
                      : 'border-white/20 bg-white/5 hover:border-white/40'
                  }`}
                >
                  ❌ False
                </button>
              </div>
            </div>
          )}

          {result && (
            <div className={`mt-6 p-6 rounded-lg border-2 ${
              result.correct
                ? 'border-green-500 bg-green-500/10'
                : 'border-red-500 bg-red-500/10'
            }`}>
              <div className="flex items-center justify-between mb-4">
                <div className="text-2xl font-bold">
                  {result.correct ? '🎉 Correct!' : '❌ Incorrect'}
                </div>
                <div className="text-xl font-bold text-accent-400">
                  +{result.points_awarded} points
                </div>
              </div>
              {result.explanation && (
                <p className="text-gray-300">{result.explanation}</p>
              )}
            </div>
          )}

          <div className="mt-6 flex justify-between">
            <button
              onClick={() => navigate('/')}
              className="btn-secondary"
            >
              ← Back to Dashboard
            </button>
            
            {!result ? (
              <button
                onClick={handleSubmit}
                disabled={
                  submitting ||
                  (question.question_type === 'MCQ' && selectedAnswer === null) ||
                  (question.question_type === 'CODING' && !codeAnswer.trim()) ||
                  (question.question_type === 'QUICK' && !textAnswer)
                }
                className="btn-primary"
              >
                {submitting ? 'Submitting...' : '✅ Submit Answer'}
              </button>
            ) : (
              <button onClick={handleNext} className="btn-primary">
                {currentIndex < questions.length - 1 ? 'Next Question →' : 'Finish Quiz 🏁'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default QuizPlayer;
