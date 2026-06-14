````md
# 🚀 CI/CD Flask Application

[![CI Pipeline](https://img.shields.io/badge/CI-Passing-brightgreen)]()
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue)]()
[![Python](https://img.shields.io/badge/Python-3.12-yellow)]()

## 🌐 Live Demo

**Application URL**

https://cicd-flask-app-himd.onrender.com

**Health Endpoint**

https://cicd-flask-app-himd.onrender.com/health

---

## 📌 Overview

A production-style DevOps project demonstrating the complete software delivery lifecycle:

- Flask Application Development
- Automated Testing with Pytest
- Docker Containerization
- Git Version Control
- GitHub Actions CI Pipeline
- Docker Hub Image Registry
- Cloud Deployment using Render

---

## 🏗️ Architecture

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions CI
    │
    ├── Install Dependencies
    ├── Run Pytest
    └── Validate Application
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
````

---

## 🛠️ Tech Stack

| Category         | Technology     |
| ---------------- | -------------- |
| Backend          | Flask          |
| Language         | Python         |
| Testing          | Pytest         |
| Containerization | Docker         |
| Version Control  | Git & GitHub   |
| CI/CD            | GitHub Actions |
| Registry         | Docker Hub     |
| Deployment       | Render         |

---

## 📂 Project Structure

```text
cicd-flask-app/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── tests/
│   └── test_app.py
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── app.py
└── README.md
```

---

## 🔍 API Endpoints

### Root Endpoint

```http
GET /
```

Response

```json
{
  "message": "CI/CD Pipeline Project",
  "status": "running"
}
```

### Health Endpoint

```http
GET /health
```

Response

```json
{
  "status": "healthy"
}
```

---

## 🧪 Running Tests

```bash
pytest -v
```

Expected Output

```text
tests/test_app.py::test_home PASSED
tests/test_app.py::test_health PASSED
```

---

## 🐳 Docker Commands

Build Image

```bash
docker build -t cicd-flask-app .
```

Run Container

```bash
docker run -p 5000:5000 cicd-flask-app
```

Push Image

```bash
docker push chandrashekharhs/cicd-flask-app:v1
```

---

## ⚙️ CI Pipeline

The GitHub Actions workflow automatically:

1. Triggers on push to main
2. Checks out source code
3. Installs dependencies
4. Runs Pytest
5. Validates application

---

## 🚀 Deployment Flow

```text
Code Change
    ↓
Git Push
    ↓
GitHub Actions
    ↓
Automated Testing
    ↓
Docker Build
    ↓
Docker Hub
    ↓
Render Deployment
    ↓
Live Application
```

---

## 🎯 Skills Demonstrated

* Linux Fundamentals
* Git & GitHub
* Python Development
* Flask APIs
* Docker
* GitHub Actions
* CI/CD
* Cloud Deployment
* Debugging & Troubleshooting

---

## 📈 Future Enhancements

* Automatic Docker Hub Publishing
* Prometheus Monitoring
* Grafana Dashboards
* Alertmanager Integration
* Kubernetes Deployment
* Terraform Infrastructure

---

## 👨‍💻 Author

**Chandrashekhar H S**

GitHub: https://github.com/Chandrashekhar-cloud

Aspiring DevOps / SRE Engineer

```
```
