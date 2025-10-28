# 🕹️ Coding Quiz Battle Arena

A full-stack web application for testing programming knowledge through interactive quizzes with real-time battles, leaderboards, and achievement tracking. Built with Django REST Framework and React, containerized with Docker.

## 🌌 Overview

Step into the **Quiz Battle Arena** – a universe where coding knowledge meets competitive gameplay. Battle through 380+ questions across 10 categories, climb the leaderboards, and prove your programming mastery. Whether you're a beginner or a seasoned developer, there's a challenge waiting for you.

**Key Highlights:**
- 🎯 380+ Questions across 10 categories (Programming Fundamentals, Web Development, Database & SQL, Computer Networks, Operating Systems, Data Structures & Algorithms, Cybersecurity, DevOps & Cloud, Software Engineering, Tech Trivia)
- 🔐 JWT Authentication with role-based access control (Admin/User)
- 📊 Real-time leaderboards (Overall, Weekly, Daily)
- 👑 Admin dashboard for complete CRUD operations
- 🎨 Responsive UI with Tailwind CSS and animations
- 🐳 Docker containerized deployment

---

## 🧿 User Roles

### Admin Role
- Full access to Django Admin panel (`/admin`)
- Custom React Admin Dashboard with:
  - **Question Management** - Create, read, update, delete questions
  - **Category Management** - Manage quiz categories
  - **User Management** - Toggle user status, change roles, view statistics
- Access to platform analytics and statistics
- Cannot participate in quizzes or challenges

**Admin Account:**
- Username: `admin`
- Password: `admin123`

### User Role
- Register and authenticate via JWT tokens
- Take quizzes across multiple categories
- Submit answers and earn points
- View personal progress and statistics
- Access leaderboards (overall, weekly, daily)

**Demo User Accounts** (password: `demo1234`):
- `alice_coder` (1500 points)
- `bob_dev` (1200 points)
- `charlie_eng` (900 points)
- `diana_prog` (600 points)
- `eve_tech` (300 points)

---

## 🏗️ Project Structure

```
quiz-battle-arena/
├── backend/
│   ├── app/                        # Django project settings
│   │   ├── settings.py            # Main configuration
│   │   ├── urls.py                # Root URL routing
│   │   ├── wsgi.py                # WSGI entry point
│   │   └── asgi.py                # ASGI for WebSockets
│   ├── core/                       # Main Django app
│   │   ├── models.py              # Category, Question, UserProfile, Score, Challenge
│   │   ├── serializers.py         # DRF serializers
│   │   ├── views.py               # API views & business logic
│   │   ├── urls.py                # API routes
│   │   ├── admin.py               # Django admin configuration
│   │   ├── permissions.py         # Role-based permissions
│   │   ├── signals.py             # Auto-create user profiles
│   │   └── management/
│   │       └── commands/
│   │           └── seed_questions.py  # Data seeding script
│   ├── requirements.txt           # Python dependencies
│   ├── Dockerfile                 # Backend container config
│   └── manage.py                  # Django CLI
├── frontend/
│   ├── src/
│   │   ├── components/            # React components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── QuizPlayer.jsx
│   │   │   ├── Leaderboard.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── AdminQuestions.jsx
│   │   │   ├── AdminCategories.jsx
│   │   │   ├── AdminUsers.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   └── BattlePlaceholder.jsx
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx   # Authentication state management
│   │   ├── api.js                # API helper functions
│   │   ├── App.jsx               # Main app component
│   │   └── index.js              # React entry point
│   ├── public/
│   │   └── index.html
│   ├── package.json              # Node dependencies
│   ├── tailwind.config.js        # Tailwind CSS config
│   ├── postcss.config.js
│   └── Dockerfile                # Frontend container config
├── docker-compose.yml            # Multi-container orchestration
├── start.sh                      # Local development script
└── README.md
```

---

## 🧰 Tech Stack

### Backend
- **Python 3.11** - Programming language
- **Django 4.2+** - Web framework
- **Django REST Framework** - RESTful API
- **djangorestframework-simplejwt** - JWT authentication
- **django-cors-headers** - CORS support
- **Django Channels** - WebSocket support (ready for multiplayer)
- **SQLite** - Default database (development)
- **MySQL 8** - Production database
- **Gunicorn** - Production WSGI server

### Frontend
- **Node.js 18+** - JavaScript runtime
- **React 18** - UI library
- **React Router v6** - Client-side routing
- **Axios** - HTTP client for API requests
- **Tailwind CSS** - Utility-first CSS framework
- **canvas-confetti** - Celebration animations

### DevOps & Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Git** - Version control

---

## 💠 How to Run Locally (PC/Laptop)

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/quiz-battle-arena.git
cd quiz-battle-arena
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Seed questions and demo users
python manage.py seed_questions

# Start Django backend server
python manage.py runserver
```

**Backend will be running on:** `http://localhost:8000`

### Step 3: Frontend Setup

Open a **new terminal window**:

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start React development server
npm start
```

**Frontend will be running on:** `http://localhost:3000`

### Step 4: Access the Application

- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **Django Admin Panel:** http://localhost:8000/admin
  - Username: `admin`
  - Password: `admin123`

---

## 🧬 How to Run with Docker

### Prerequisites
- Docker Desktop installed
- Docker Compose installed

### Step 1: Build Docker Images

Navigate to the project root directory and build the images:

```bash
# Build backend image
docker build -t quiz-backend ./backend

# Build frontend image
docker build -t quiz-frontend ./frontend
```

### Step 2: Run with Docker Compose

The easiest way to run all services together:

```bash
# Build and start all services (MySQL, Backend, Frontend)
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Step 3: Access the Application

After Docker Compose starts successfully:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **Admin Panel:** http://localhost:8000/admin

### Docker Services

Docker Compose will start 3 services:

1. **MySQL Database** (port 3306)
   - Database: `quizdb`
   - User: `quizuser`
   - Password: `quizpassword`

2. **Django Backend** (port 8000)
   - Runs migrations automatically
   - Seeds questions on startup
   - Uses Gunicorn with 4 workers

3. **React Frontend** (port 3000)
   - Production build served via `serve`

### Manual Docker Commands

If you prefer to run containers individually:

```bash
# 1. Start MySQL container
docker run -d \
  --name quiz-mysql \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=quizdb \
  -e MYSQL_USER=quizuser \
  -e MYSQL_PASSWORD=quizpassword \
  -p 3306:3306 \
  mysql:8

# 2. Wait for MySQL to be ready (about 30 seconds), then start backend
docker run -d \
  --name quiz-backend \
  -e DATABASE_ENGINE=mysql \
  -e DATABASE_HOST=quiz-mysql \
  -e DATABASE_NAME=quizdb \
  -e DATABASE_USER=quizuser \
  -e DATABASE_PASSWORD=quizpassword \
  -p 8000:8000 \
  --link quiz-mysql \
  quiz-backend

# 3. Start frontend
docker run -d \
  --name quiz-frontend \
  -p 3000:3000 \
  quiz-frontend
```

### Useful Docker Commands

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View logs for a specific container
docker logs quiz-backend
docker logs quiz-frontend
docker logs quiz-mysql

# Stop a container
docker stop quiz-backend

# Start a stopped container
docker start quiz-backend

# Remove a container
docker rm quiz-backend

# Remove an image
docker rmi quiz-backend

# View Docker images
docker images

# Clean up (remove all stopped containers, unused images, etc.)
docker system prune -a
```

### Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes (deletes database data)
docker-compose down -v

# Rebuild images
docker-compose build

# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend

# Restart a service
docker-compose restart backend

# View running services
docker-compose ps
```

---

<div align="center">

**Made with 🩶 for coders who live for the challenge** 🕹️

*Enter the Arena. Prove Your Skills. Dominate the Leaderboard.*

</div>