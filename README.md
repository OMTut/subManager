# Subscription Manager

A modern subscription management application built with React frontend and FastAPI backend.

## 🏗️ Architecture

- **Frontend**: React + Vite, served with nginx
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Deployment**: Kubernetes (GitOps ready)

## 🚀 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd subManager
   ```

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:80
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Building Individual Images

**Frontend:**
```bash
cd frontend
docker build -t submanager-frontend .
```

**Backend API:**
```bash
cd api
docker build -t submanager-api .
```

## 📦 Container Images

When pushed to GitHub, the CI/CD pipeline automatically builds and pushes images to GitHub Container Registry:

- `ghcr.io/[username]/submanager/frontend:latest`
- `ghcr.io/[username]/submanager/api:latest`

## 🎯 Kubernetes Deployment

### Image References for K8s Manifests

Use these image references in your Kubernetes YAML files:

```yaml
# Frontend Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: submanager-frontend
spec:
  template:
    spec:
      containers:
      - name: frontend
        image: ghcr.io/[username]/submanager/frontend:latest
        ports:
        - containerPort: 80

---
# API Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: submanager-api
spec:
  template:
    spec:
      containers:
      - name: api
        image: ghcr.io/[username]/submanager/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          value: "postgres-service"
        - name: DB_NAME
          value: "subscription_manager"
```

## 🔧 Environment Variables

### Frontend
- `VITE_API_BASE_URL`: Backend API URL (default: http://localhost:8000)

### Backend API
- `DB_HOST`: PostgreSQL host
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_PORT`: Database port (default: 5432)

## 🏥 Health Checks

Both containers include health check endpoints:

- **Frontend**: `GET /health`
- **API**: `GET /health`

These are used by:
- Docker Compose health checks
- Kubernetes liveness/readiness probes
- Load balancers

## 🔄 GitOps Workflow

1. **Push code** to GitHub repository
2. **GitHub Actions** builds and pushes Docker images
3. **Update K8s manifests** with new image tags
4. **ArgoCD/Flux** detects changes and deploys to cluster

## 📁 File Structure

```
subManager/
├── frontend/
│   ├── Dockerfile              # Multi-stage build with nginx
│   ├── nginx.conf             # nginx configuration for SPA
│   └── .dockerignore          # Frontend build exclusions
├── api/
│   ├── Dockerfile             # Python FastAPI container
│   ├── requirements.txt       # Python dependencies
│   └── .dockerignore          # API build exclusions
├── docker-compose.yml         # Local development stack
├── .github/workflows/ci-cd.yml # CI/CD pipeline
└── README.md                  # This file
```

## 🎨 Features

- ✅ Modern React UI with peacock blue theme
- ✅ FastAPI backend with automatic OpenAPI docs
- ✅ PostgreSQL database with proper schema
- ✅ Docker containerization for all components
- ✅ Health checks and monitoring endpoints
- ✅ CI/CD pipeline with GitHub Actions
- ✅ GitOps ready for Kubernetes deployment
- ✅ Production-ready nginx configuration
- ✅ Security best practices (non-root containers, etc.)

## 🚦 Next Steps for Kubernetes

1. **Create namespace**
2. **Set up database** (managed or in-cluster)
3. **Create secrets** for database credentials
4. **Deploy backend** with proper environment variables
5. **Deploy frontend** with API endpoint configuration
6. **Set up ingress** for external access
7. **Configure GitOps** tool to watch your manifests

Happy deploying! 🚀

