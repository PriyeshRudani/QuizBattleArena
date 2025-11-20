# 🚀 Kubernetes Deployment Guide - QuizBattleArena

## Prerequisites

1. **Docker Desktop** with Kubernetes enabled
   - Open Docker Desktop → Settings → Kubernetes → Enable Kubernetes
   - Wait for Kubernetes to start (green indicator)

2. **kubectl** installed (comes with Docker Desktop)
   ```powershell
   kubectl version --client
   ```

## 📦 Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│         Namespace: quiz-battle-arena                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐    ┌──────────────┐             │
│  │   Frontend   │───▶│   Backend    │             │
│  │  (React)     │    │  (Django)    │             │
│  │  Port: 30000 │    │  Port: 30800 │             │
│  │  Replicas: 2 │    │  Replicas: 2 │             │
│  └──────────────┘    └──────┬───────┘             │
│                              │                      │
│                              ▼                      │
│                     ┌──────────────┐               │
│                     │    MySQL     │               │
│                     │  Port: 3306  │               │
│                     │  Replicas: 1 │               │
│                     │  + PVC (5GB) │               │
│                     └──────────────┘               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🎯 Quick Deploy (All-in-One)

```powershell
# Deploy everything
kubectl apply -f k8s/

# Check deployment status
kubectl get all -n quiz-battle-arena

# Watch pods until all are running
kubectl get pods -n quiz-battle-arena -w
```

## 📋 Step-by-Step Deployment

### Step 1: Create Namespace
```powershell
kubectl apply -f k8s/namespace.yaml
```

### Step 2: Create Secrets and ConfigMap
```powershell
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmap.yaml
```

### Step 3: Deploy MySQL
```powershell
# Create persistent volume claim
kubectl apply -f k8s/mysql-pvc.yaml

# Deploy MySQL
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mysql-service.yaml

# Wait for MySQL to be ready (may take 30-60 seconds)
kubectl wait --for=condition=ready pod -l app=mysql -n quiz-battle-arena --timeout=120s
```

### Step 4: Deploy Backend
```powershell
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml

# Wait for backend to be ready
kubectl wait --for=condition=ready pod -l app=backend -n quiz-battle-arena --timeout=120s
```

### Step 5: Deploy Frontend
```powershell
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

# Wait for frontend to be ready
kubectl wait --for=condition=ready pod -l app=frontend -n quiz-battle-arena --timeout=120s
```

## ✅ Verify Deployment

### Check All Resources
```powershell
# View all resources
kubectl get all -n quiz-battle-arena

# Check pods status
kubectl get pods -n quiz-battle-arena

# Check services
kubectl get svc -n quiz-battle-arena

# Check persistent volume claims
kubectl get pvc -n quiz-battle-arena
```

### Expected Output:
```
NAME                            READY   STATUS    RESTARTS   AGE
pod/backend-xxxxxxxxxx-xxxxx    1/1     Running   0          2m
pod/backend-xxxxxxxxxx-xxxxx    1/1     Running   0          2m
pod/frontend-xxxxxxxxxx-xxxxx   1/1     Running   0          1m
pod/frontend-xxxxxxxxxx-xxxxx   1/1     Running   0          1m
pod/mysql-xxxxxxxxxx-xxxxx      1/1     Running   0          3m
```

## 🌐 Access the Application

### Frontend (React App)
```
http://localhost:30000
```

### Backend API
```
http://localhost:30800/api
```

### MySQL (Direct Access - Optional)
```
Host: localhost
Port: 30306
Username: quizuser
Password: quizpassword
Database: quizdb
```

## 🔍 Monitoring and Debugging

### View Logs
```powershell
# Backend logs
kubectl logs -f deployment/backend -n quiz-battle-arena

# Frontend logs
kubectl logs -f deployment/frontend -n quiz-battle-arena

# MySQL logs
kubectl logs -f deployment/mysql -n quiz-battle-arena

# Logs from specific pod
kubectl logs -f <pod-name> -n quiz-battle-arena
```

### Execute Commands Inside Pods
```powershell
# Shell into backend pod
kubectl exec -it deployment/backend -n quiz-battle-arena -- bash

# Run Django migrations manually
kubectl exec -it deployment/backend -n quiz-battle-arena -- python manage.py migrate

# Create superuser
kubectl exec -it deployment/backend -n quiz-battle-arena -- python manage.py createsuperuser

# Shell into MySQL
kubectl exec -it deployment/mysql -n quiz-battle-arena -- mysql -u quizuser -p
```

### Check Events
```powershell
# View namespace events
kubectl get events -n quiz-battle-arena --sort-by='.lastTimestamp'

# Describe a specific resource
kubectl describe pod <pod-name> -n quiz-battle-arena
kubectl describe deployment backend -n quiz-battle-arena
```

## 🔄 Update Application

### Update Docker Images
```powershell
# After building and pushing new images to Docker Hub
kubectl rollout restart deployment/backend -n quiz-battle-arena
kubectl rollout restart deployment/frontend -n quiz-battle-arena

# Check rollout status
kubectl rollout status deployment/backend -n quiz-battle-arena
kubectl rollout status deployment/frontend -n quiz-battle-arena
```

### Scale Deployments
```powershell
# Scale backend
kubectl scale deployment backend --replicas=3 -n quiz-battle-arena

# Scale frontend
kubectl scale deployment frontend --replicas=3 -n quiz-battle-arena
```

## 🗑️ Clean Up

### Delete Everything
```powershell
# Delete all resources in namespace
kubectl delete namespace quiz-battle-arena

# Or delete resources individually
kubectl delete -f k8s/
```

### Delete Specific Resources
```powershell
# Delete frontend only
kubectl delete -f k8s/frontend-deployment.yaml
kubectl delete -f k8s/frontend-service.yaml

# Delete backend only
kubectl delete -f k8s/backend-deployment.yaml
kubectl delete -f k8s/backend-service.yaml
```

## 🐛 Common Issues and Solutions

### Issue: Pods stuck in "Pending" state
```powershell
# Check pod details
kubectl describe pod <pod-name> -n quiz-battle-arena

# Common causes:
# - PVC not bound (check: kubectl get pvc -n quiz-battle-arena)
# - Insufficient resources
# - Image pull errors
```

### Issue: Pods in "CrashLoopBackOff"
```powershell
# View logs to see the error
kubectl logs <pod-name> -n quiz-battle-arena

# Common causes:
# - Backend can't connect to MySQL (MySQL not ready yet)
# - Environment variables incorrect
# - Application error
```

### Issue: Can't access application at localhost:30000
```powershell
# Verify service is running
kubectl get svc -n quiz-battle-arena

# Check if Kubernetes is running in Docker Desktop
kubectl cluster-info

# Try port-forward as alternative
kubectl port-forward -n quiz-battle-arena svc/frontend-service 3000:3000
kubectl port-forward -n quiz-battle-arena svc/backend-service 8000:8000
```

### Issue: MySQL data lost after pod restart
```powershell
# Check PVC status
kubectl get pvc -n quiz-battle-arena

# PVC should be "Bound" status
# If not bound, check storage class:
kubectl get storageclass
```

## 📊 Resource Usage

### View Resource Consumption
```powershell
# CPU and Memory usage
kubectl top pods -n quiz-battle-arena

# Node resource usage
kubectl top nodes
```

## 🔐 Security Notes

**⚠️ Important for Production:**

1. **Change default passwords** in `k8s/secrets.yaml`
   ```powershell
   # Encode new password
   echo -n "your-new-password" | base64
   ```

2. **Use proper secret management** (e.g., Azure Key Vault, AWS Secrets Manager)

3. **Enable RBAC** and create service accounts with limited permissions

4. **Add network policies** to restrict pod-to-pod communication

5. **Use ingress with TLS** instead of NodePort for production

## 📝 Configuration Files

| File | Purpose |
|------|---------|
| `namespace.yaml` | Creates isolated namespace |
| `secrets.yaml` | Stores sensitive data (passwords) |
| `configmap.yaml` | Stores configuration variables |
| `mysql-pvc.yaml` | Persistent storage for MySQL |
| `mysql-deployment.yaml` | MySQL database deployment |
| `mysql-service.yaml` | MySQL service (internal + NodePort) |
| `backend-deployment.yaml` | Django backend deployment |
| `backend-service.yaml` | Backend NodePort service |
| `frontend-deployment.yaml` | React frontend deployment |
| `frontend-service.yaml` | Frontend NodePort service |

## 🎓 Learning Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Docker Desktop Kubernetes](https://docs.docker.com/desktop/kubernetes/)

## 🆘 Get Help

```powershell
# Kubernetes version and cluster info
kubectl version
kubectl cluster-info

# List all resources
kubectl api-resources

# Get help for a command
kubectl help
kubectl apply --help
```

---

**Happy Deploying! 🚀**
