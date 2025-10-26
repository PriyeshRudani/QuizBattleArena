#!/usr/bin/env bash

# Coding Quiz Battle Arena - Startup Script
echo "🎮 Starting Coding Quiz Battle Arena..."

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Created superuser: admin/admin123')
"

# Seed questions
echo "🌱 Seeding questions..."
python manage.py seed_questions

# Start Django server in background
echo "🚀 Starting Django backend on port 8000..."
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Frontend setup
echo "📦 Setting up frontend..."
cd ../frontend

# Install Node dependencies
npm install

# Start React development server
echo "🚀 Starting React frontend on port 5000..."
PORT=5000 BROWSER=none npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Application started successfully!"
echo "🌐 Frontend: http://localhost:5000"
echo "🔧 Backend API: http://localhost:8000/api"
echo "🔐 Admin Panel: http://localhost:8000/admin (admin/admin123)"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
