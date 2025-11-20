# Docker Hub Push Script for QuizBattleArena
# Replace 'yourusername' with your actual Docker Hub username

$DOCKER_USERNAME = Read-Host "Enter your Docker Hub username"
$PROJECT_NAME = "quizbattlearena"

Write-Host "Building and pushing Docker images to Docker Hub..." -ForegroundColor Green

# Build and push backend
Write-Host "`nBuilding backend image..." -ForegroundColor Cyan
docker build -t ${DOCKER_USERNAME}/${PROJECT_NAME}-backend:latest ./backend
Write-Host "Pushing backend image..." -ForegroundColor Cyan
docker push ${DOCKER_USERNAME}/${PROJECT_NAME}-backend:latest

# Build and push frontend
Write-Host "`nBuilding frontend image..." -ForegroundColor Cyan
docker build -t ${DOCKER_USERNAME}/${PROJECT_NAME}-frontend:latest ./frontend
Write-Host "Pushing frontend image..." -ForegroundColor Cyan
docker push ${DOCKER_USERNAME}/${PROJECT_NAME}-frontend:latest

Write-Host "`n✅ Done! Your Docker Hub links are:" -ForegroundColor Green
Write-Host "Backend:  https://hub.docker.com/r/${DOCKER_USERNAME}/${PROJECT_NAME}-backend" -ForegroundColor Yellow
Write-Host "Frontend: https://hub.docker.com/r/${DOCKER_USERNAME}/${PROJECT_NAME}-frontend" -ForegroundColor Yellow
Write-Host "`nDocker pull commands:" -ForegroundColor Green
Write-Host "docker pull ${DOCKER_USERNAME}/${PROJECT_NAME}-backend:latest"
Write-Host "docker pull ${DOCKER_USERNAME}/${PROJECT_NAME}-frontend:latest"
