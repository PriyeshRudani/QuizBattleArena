# Docker Hub Deployment Guide

## 🚀 Quick Start - Push to Docker Hub

### Prerequisites
1. Create a Docker Hub account at https://hub.docker.com
2. Install Docker Desktop on your machine

### Steps to Push Images

1. **Login to Docker Hub**
   ```powershell
   docker login
   ```
   Enter your Docker Hub username and password when prompted.

2. **Run the automated push script**
   ```powershell
   .\docker-push.ps1
   ```
   This will:
   - Build both backend and frontend images
   - Tag them with your Docker Hub username
   - Push them to Docker Hub
   - Display your Docker Hub links

### Manual Method (Alternative)

If you prefer to do it manually:

```powershell
# Replace 'yourusername' with your Docker Hub username
$USERNAME = "yourusername"

# Build images
docker build -t ${USERNAME}/quizbattlearena-backend:latest ./backend
docker build -t ${USERNAME}/quizbattlearena-frontend:latest ./frontend

# Push to Docker Hub
docker push ${USERNAME}/quizbattlearena-backend:latest
docker push ${USERNAME}/quizbattlearena-frontend:latest
```

## 📦 Your Docker Hub Links

After pushing, your images will be available at:

- **Backend:** `https://hub.docker.com/r/yourusername/quizbattlearena-backend`
- **Frontend:** `https://hub.docker.com/r/yourusername/quizbattlearena-frontend`

Replace `yourusername` with your actual Docker Hub username.

## 🎯 For Submission

Use these links in your submission sheet:

**Docker Hub Image Links:**
- Backend: `docker pull yourusername/quizbattlearena-backend:latest`
- Frontend: `docker pull yourusername/quizbattlearena-frontend:latest`

Or provide the Docker Hub repository URLs:
- `https://hub.docker.com/r/yourusername/quizbattlearena-backend`
- `https://hub.docker.com/r/yourusername/quizbattlearena-frontend`

## 🔧 Deploy from Docker Hub

To deploy using the Docker Hub images:

```powershell
# Use the production docker-compose file
docker-compose -f docker-compose.prod.yml up -d
```

Make sure to update the `yourusername` in `docker-compose.prod.yml` with your actual Docker Hub username.

## 📝 Notes

- The images include both backend (Django) and frontend (React) applications
- Database (MySQL) uses the official MySQL image from Docker Hub
- Make sure your images are set to **public** visibility on Docker Hub for easy access
- Total size: Backend ~500MB, Frontend ~150MB (approximate)

## 🆘 Troubleshooting

**Issue: "denied: requested access to the resource is denied"**
- Solution: Make sure you're logged in with `docker login`

**Issue: "Cannot connect to Docker daemon"**
- Solution: Make sure Docker Desktop is running

**Issue: Build fails**
- Solution: Check if all dependencies are properly listed in requirements.txt and package.json
