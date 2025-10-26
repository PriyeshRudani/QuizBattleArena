# 🎮 Coding Quiz Battle Arena

A full-stack web application for testing programming knowledge through interactive quizzes with real-time battles, leaderboards, and achievement tracking.

## 🌟 Features

### ✅ MVP Features (Replit Ready)
- **Django REST Framework** backend with JWT authentication
- **React** frontend with Tailwind CSS and playful animations
- **10 Quiz Categories**: Programming Fundamentals, Web Development, Database & SQL, Computer Networks, Operating Systems, Data Structures & Algorithms, Cybersecurity, DevOps & Cloud, Software Engineering, Tech Trivia
- **380+ Questions**: 300 MCQs, 30 coding challenges, 50 quick-fire questions
- **User Authentication**: Register, login, profile management
- **Quiz System**: Adaptive quiz player with timer and confetti animations
- **Leaderboard**: Overall, weekly, and daily rankings
- **Django Admin**: Full CRUD interface for managing questions
- **Responsive Design**: Mobile-first UI with hover effects and transitions

### 🚀 Future Features
- Real-time multiplayer battles (Django Channels + WebSocket)
- Advanced code execution sandbox
- Badge and achievement system
- Challenge creation and matchmaking
- Live chat during battles

## 📁 Project Structure

```
quiz-battle-arena/
├── backend/
│   ├── app/                    # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── core/                   # Main Django app
│   │   ├── models.py          # Category, Question, UserProfile, Score, Challenge
│   │   ├── serializers.py     # DRF serializers
│   │   ├── views.py           # API views
│   │   ├── urls.py            # API routes
│   │   ├── admin.py           # Admin configuration
│   │   └── management/
│   │       └── commands/
│   │           └── seed_questions.py  # Data seeding script
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── QuizPlayer.jsx
│   │   │   ├── Leaderboard.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── BattlePlaceholder.jsx
│   │   ├── api.js            # API helper functions
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
├── start.sh                   # Replit startup script
└── README.md
```

## 🚀 Running on Replit

### Quick Start

1. Click the **Run** button or execute:
   ```bash
   bash start.sh
   ```

2. The script will:
   - Install Python dependencies
   - Run database migrations
   - Create admin user (admin/admin123)
   - Seed 380+ questions
   - Start Django backend (port 8000)
   - Install Node dependencies
   - Start React frontend (port 5000)

3. Access the application:
   - **Frontend**: http://localhost:5000
   - **Backend API**: http://localhost:8000/api
   - **Admin Panel**: http://localhost:8000/admin (username: `admin`, password: `admin123`)

### Demo Users

Login with these pre-seeded accounts (password: `demo1234`):
- `alice_coder` (1500 points)
- `bob_dev` (1200 points)
- `charlie_eng` (900 points)
- `diana_prog` (600 points)
- `eve_tech` (300 points)

## 📥 Download & Local Development

### Step 1: Download from Replit

1. Click the three dots menu in Replit
2. Select **Download as zip**
3. Extract the zip file on your local machine

### Step 2: Set Up Python Virtual Environment

```bash
cd quiz-battle-arena
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### Step 3: Switch to MySQL (Optional)

#### Option A: Using Docker MySQL

```bash
docker run --name quiz-mysql \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=quizdb \
  -e MYSQL_USER=quizuser \
  -e MYSQL_PASSWORD=quizpassword \
  -p 3306:3306 \
  -d mysql:8
```

#### Option B: Local MySQL Installation

Install MySQL locally and create a database:

```sql
CREATE DATABASE quizdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'quizuser'@'localhost' IDENTIFIED BY 'quizpassword';
GRANT ALL PRIVILEGES ON quizdb.* TO 'quizuser'@'localhost';
FLUSH PRIVILEGES;
```

#### Configure Django for MySQL

Create `backend/.env` file:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here

DATABASE_ENGINE=mysql
DATABASE_NAME=quizdb
DATABASE_USER=quizuser
DATABASE_PASSWORD=quizpassword
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

Update `backend/app/settings.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME', 'quizdb'),
        'USER': os.getenv('DATABASE_USER', 'quizuser'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'quizpassword'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

Install MySQL client:

```bash
pip install mysqlclient
```

Run migrations:

```bash
python manage.py migrate
python manage.py seed_questions
python manage.py createsuperuser
```

## 🐳 Docker Deployment

### Build and Run with Docker Compose

```bash
# Create .env file with database credentials
cp backend/.env.example .env

# Edit .env with your settings
nano .env

# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin: http://localhost:8000/admin

### Individual Docker Commands

Build images:
```bash
# Backend
docker build -t quiz-backend ./backend

# Frontend
docker build -t quiz-frontend ./frontend
```

Run containers:
```bash
# MySQL
docker run -d --name quiz-mysql \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=quizdb \
  -p 3306:3306 \
  mysql:8

# Backend
docker run -d --name quiz-backend \
  -e DATABASE_HOST=quiz-mysql \
  -p 8000:8000 \
  --link quiz-mysql \
  quiz-backend

# Frontend
docker run -d --name quiz-frontend \
  -p 3000:3000 \
  --link quiz-backend \
  quiz-frontend
```

## ☸️ Kubernetes Deployment

### Create Kubernetes Manifests

```bash
mkdir k8s
```

**k8s/mysql-deployment.yaml**:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec:
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "rootpassword"
        - name: MYSQL_DATABASE
          value: "quizdb"
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: mysql-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-storage
        persistentVolumeClaim:
          claimName: mysql-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  ports:
  - port: 3306
  selector:
    app: mysql
```

**k8s/backend-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quiz-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: quiz-backend
  template:
    metadata:
      labels:
        app: quiz-backend
    spec:
      containers:
      - name: backend
        image: quiz-backend:latest
        env:
        - name: DATABASE_HOST
          value: "mysql"
        - name: DATABASE_NAME
          value: "quizdb"
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: quiz-backend
spec:
  type: LoadBalancer
  ports:
  - port: 8000
    targetPort: 8000
  selector:
    app: quiz-backend
```

**k8s/frontend-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quiz-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: quiz-frontend
  template:
    metadata:
      labels:
        app: quiz-frontend
    spec:
      containers:
      - name: frontend
        image: quiz-frontend:latest
        ports:
        - containerPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: quiz-frontend
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 3000
  selector:
    app: quiz-frontend
```

Deploy to Kubernetes:
```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get services
```

## 📚 API Endpoints

### Authentication
- `POST /api/auth/login/` - Login with username/password
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/refresh/` - Refresh JWT token

### Categories
- `GET /api/categories/` - List all categories
- `GET /api/categories/{slug}/questions/` - Get questions for category

### Questions
- `GET /api/questions/` - List all questions
- `GET /api/questions/{id}/` - Get question details
- `POST /api/questions/{id}/submit/` - Submit answer

### User
- `GET /api/user/profile/` - Get user profile

### Leaderboard
- `GET /api/leaderboard/?period=overall|weekly|daily` - Get leaderboard

### Challenges
- `POST /api/challenges/` - Create challenge
- `GET /api/challenges/` - List user challenges
- `GET /api/challenges/{id}/status/` - Get challenge status

## 🛠️ Tech Stack

### Backend
- **Django 4.2+** - Web framework
- **Django REST Framework** - API
- **djangorestframework-simplejwt** - JWT authentication
- **django-cors-headers** - CORS support
- **Django Channels** - WebSocket support (placeholder)
- **SQLite** - Default database (Replit)
- **MySQL** - Production database
- **Gunicorn** - WSGI server

### Frontend
- **React 18** - UI library
- **React Router** - Navigation
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **canvas-confetti** - Animations

## 🔧 Development

### Backend Development

```bash
cd backend

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed questions
python manage.py seed_questions

# Run development server
python manage.py runserver
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm start

# Build for production
npm run build
```

## 📝 Environment Variables

### Backend (.env)
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_ENGINE=sqlite3|mysql|postgresql
DATABASE_NAME=quizdb
DATABASE_USER=quizuser
DATABASE_PASSWORD=quizpassword
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built on Replit for rapid prototyping
- Designed for easy migration to production environments
- Ready for Kubernetes scaling

## 📧 Support

For issues and questions:
- Check the documentation
- Review existing issues
- Create a new issue with detailed information

---

**Made with ❤️ for coders who love to challenge themselves!** 🎮
