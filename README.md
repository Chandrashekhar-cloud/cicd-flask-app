# 🚀 DevOps Task Manager API with CI/CD Pipeline

> Production-style Flask Task Manager API demonstrating Docker, Automated Testing, GitHub Actions, Monitoring Endpoints, and Cloud Deployment.

---

## 🌐 Live Demo

### Application URL

https://cicd-flask-app-himd.onrender.com

### Health Endpoint

https://cicd-flask-app-himd.onrender.com/health

### Metrics Endpoint

https://cicd-flask-app-himd.onrender.com/metrics

---

## 📸 Screenshots

### Live Application

![Live Application](assets/live-app.png)

### GitHub Actions Pipeline

![GitHub Actions](assets/github-actions.png)

---

## 📌 Project Overview

This project demonstrates a complete DevOps workflow from development to production deployment.

### Features

- Task Management REST API
- CRUD Operations
- Health Monitoring
- System Statistics Endpoint
- Prometheus-style Metrics
- Automated Testing with Pytest
- Docker Containerization
- GitHub Actions CI Pipeline
- Docker Hub Image Publishing
- Cloud Deployment on Render

---

## ⚙️ Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Framework | Flask |
| Testing | Pytest |
| Monitoring | Psutil |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Registry | Docker Hub |
| Deployment | Render |
| Version Control | Git & GitHub |

---

## 🔍 API Endpoints

| Method | Endpoint | Description |
|----------|-----------|-------------|
| GET | / | Application Info |
| GET | /health | Health Check |
| GET | /api/info | Application Details |
| GET | /api/stats | System Statistics |
| GET | /api/tasks | List Tasks |
| POST | /api/tasks | Create Task |
| GET | /api/tasks/{id} | Get Task |
| PATCH | /api/tasks/{id} | Update Task |
| DELETE | /api/tasks/{id} | Delete Task |
| GET | /metrics | Monitoring Metrics |

---

## 🧪 Automated Testing

Total Tests: **16**

Run Tests:

```bash
pytest -v
```

Expected Output:

```text
==================== 16 passed ====================
```

### Test Coverage

- Health Endpoints
- API Information
- System Statistics
- Task Creation
- Task Retrieval
- Task Updates
- Task Deletion
- Error Handling
- Filtering Logic
- Metrics Endpoint

---

## 🐳 Docker Usage

Build Image:

```bash
docker build -t cicd-flask-app .
```

Run Container:

```bash
docker run -p 5000:5000 cicd-flask-app
```

Push Image:

```bash
docker push chandrashekharhs/cicd-flask-app:v1
```

---

## 🔄 CI/CD Pipeline

Every push to the `main` branch automatically:

- Installs Dependencies
- Runs Automated Tests
- Validates Application Build
- Reports Build Status
- Triggers Deployment Workflow

---

## 📊 Monitoring Features

The application provides:

- CPU Usage
- Memory Usage
- Disk Usage
- Application Uptime
- Request Counters
- Error Counters
- Task Statistics

Metrics Endpoint:

```text
/metrics
```

---

## 🚀 Deployment Flow

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Install Dependencies
    ├── Run Tests
    └── Validate Build
    │
    ▼
Docker Image
    │
    ▼
Docker Hub
    │
    ▼
Render Deployment
    │
    ▼
Live Application
```

---

## 🎯 DevOps Skills Demonstrated

- Linux Fundamentals
- Git & GitHub
- Python Development
- REST API Development
- Automated Testing
- Docker Containerization
- GitHub Actions
- Continuous Integration
- Cloud Deployment
- Monitoring & Metrics
- Troubleshooting
- DevOps Workflow Automation

---

## 📈 Future Improvements

- Prometheus Integration
- Grafana Dashboards
- Kubernetes Deployment
- Helm Charts
- Terraform Infrastructure
- GitOps with ArgoCD
- AWS EKS Deployment

---

## 👨‍💻 Author

### Chandrashekhar H S

Aspiring DevOps / Site Reliability Engineer

GitHub:
https://github.com/Chandrashekhar-cloud

Live Project:
https://cicd-flask-app-himd.onrender.com

---

⭐ If you found this project useful, consider giving it a star.
