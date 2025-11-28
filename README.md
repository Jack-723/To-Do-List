# Minimal Todo API + UI (FastAPI + SQLite)

A simple To-do list application built for my DevOps course.  
Includes a REST API (with Swagger docs) and a lightweight HTML interface.

---

## Features
- CRUD endpoints for todos (`/todos`)
- Persistent storage using SQLite (`todo.db`)
- Interactive API docs at `/docs`
- Simple web UI at `/`

---

## Tech
- Python 3.11+
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- SQLite database

---

## Quickstart

```bash
# 1. Create virtual environment
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate
# macOS/Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000/docs
 → Swagger UI (API testing)

http://127.0.0.1:8000/
 → HTML Todo UI

Notes

Made as coursework for DevOps & SDLC pipeline design.

Future improvements: tests, Dockerfile, CI/CD workflow.


---

## 🚀 Assignment 2 Updates - DevOps Enhancements

This project has been enhanced with modern DevOps practices including automated testing, CI/CD pipeline, containerization, and cloud deployment.

### New Features
- ✅ Automated unit and integration tests (93% coverage)
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Dockerized application
- ✅ Deployed to Google Cloud Run
- ✅ Prometheus metrics endpoint for monitoring

---

## 🧪 Running Tests

### Install Test Dependencies
```bash
pip install -r requirements-dev.txt
```

### Run Tests with Coverage
```bash
pytest
```

### Run Tests with Verbose Output
```bash
pytest -v
```

### View Coverage Report
```bash
pytest --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

### Coverage Requirements
- Minimum coverage: **70%**
- Current coverage: **93.81%** ✅

---

## 🐳 Running with Docker

### Build and Run with Docker Compose
```bash
docker-compose up --build
```

The app will be available at: `http://localhost:8000`

### Stop the Container

Press `Ctrl + C` or run:
```bash
docker-compose down
```

### Build Docker Image Manually
```bash
docker build -t todo-list-app .
```

### Run Docker Container Manually
```bash
docker run -p 8000:8080 todo-list-app
```

---

## ☁️ Cloud Deployment

### Live Application

The application is deployed on **Google Cloud Run**:

🌐 **Live URL:** https://todo-list-app-976425574918.europe-west1.run.app/

### Deployment Process

The app is deployed using Google Cloud Run with the following command:
```bash
gcloud run deploy todo-list-app \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated
```

### Key Features
- ✅ Automatic scaling (0 to N instances)
- ✅ Pay-per-use pricing (within free tier)
- ✅ HTTPS enabled by default
- ✅ Global CDN

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

Every push to the `main` branch triggers a fully automated CI/CD pipeline:

**Stage 1: Test** (~25 seconds)
1. ✅ Sets up Python 3.13 environment
2. ✅ Installs dependencies
3. ✅ Runs all tests with pytest
4. ✅ Measures code coverage
5. ✅ **Fails if coverage < 70%** (currently 93.81%)

**Stage 2: Build** (~30 seconds)
6. ✅ Sets up Docker Buildx
7. ✅ Builds Docker image
8. ✅ Validates containerization

**Stage 3: Deploy** (~2 minutes) - **Automated CD**
9. ✅ Authenticates to Google Cloud
10.✅ **Automatically deploys to Cloud Run**
11.✅ Updates live application with zero downtime

**Total Pipeline Time:** ~2-4 minutes from commit to production


### View CI/CD Status

Check the [Actions tab](https://github.com/Jack-723/To-Do-List/actions) in the repository to see all pipeline runs.


### Continuous Deployment (CD)

The pipeline includes fully automated deployment to Google Cloud Run.

**Automated Deployment Process:**
```yaml
deploy:
  runs-on: ubuntu-latest
  needs: build
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  
  steps:
    - Authenticate to Google Cloud (service account)
    - Set up Cloud SDK
    - Deploy to Cloud Run automatically
```

**Key Features:**
- **Fully Automated:** No manual `gcloud` commands needed
- **Conditional:** Only deploys from `main` branch pushes
- **Secure:** Uses service account credentials stored in GitHub Secrets
- **Fast:** Deployment completes in 2-4 minutes
- **Zero Downtime:** Rolling updates with health checks

**Service Account Configuration:**

A dedicated service account (`github-actions-deployer`) was created with these roles:
- **Cloud Run Admin** - Deploy and manage Cloud Run services
- **Service Account User** - Act as runtime service account
- **Storage Admin** - Access container registry
- **Artifact Registry Writer** - Push Docker images
- **Cloud Build Editor** - Build containers from source
- **Service Usage Consumer** - Use Google Cloud APIs

**Security Implementation:**
- Credentials stored encrypted in GitHub Secrets
- Never exposed in logs or code
- Principle of least privilege applied
- Service account cannot be used outside GitHub Actions

**Deployment Workflow:**
1. Developer commits code to `main` branch
2. Tests run and pass automatically
3. Docker image builds successfully
4. **GitHub Actions authenticates to Google Cloud**
5. **Deployment executes automatically via `gcloud` CLI**
6. **Live application updates with zero downtime**
7. **Total time: ~4 minutes from commit to production**


**Evidence of Working CD:**
- GitHub Actions logs show successful deployments
- Service updates visible in Cloud Run console
- Application version changes reflect automatically
- Professor can verify via Google Cloud viewer access
---

## 📊 Monitoring & Metrics

### Health Check Endpoint

Check application health:
```
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

### Metrics Endpoint

View Prometheus-compatible metrics:
```
GET /metrics
```

**Tracked Metrics:**
- `app_requests_total` - Total number of requests by method, endpoint, and status
- `app_request_latency_seconds` - Request latency histogram

### Example

**Local:**
- Health: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics

**Production:**
- Health: https://todo-list-app-976425574918.europe-west1.run.app/health
- Metrics: https://todo-list-app-976425574918.europe-west1.run.app/metrics

---

### Prometheus Configuration

A `prometheus.yml` configuration file is provided to demonstrate how to set up Prometheus to scrape metrics from the application.

**Configuration includes:**
- Local development instance (`localhost:8000`)
- Production instance (Google Cloud Run)

**To use with Prometheus:**

1. Install Prometheus: https://prometheus.io/download/
2. Run Prometheus with the config:
```bash
   prometheus --config.file=prometheus.yml
```
3. Access Prometheus UI: http://localhost:9090
4. View metrics and create dashboards

**Example Prometheus Queries:**
```promql
# Total requests
rate(app_requests_total[5m])

# Average latency
histogram_quantile(0.95, rate(app_request_latency_seconds_bucket[5m]))

# Error rate
rate(app_requests_total{status=~"5.."}[5m])
```

## 📁 Project Structure (Updated)
```
To-Do-List/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app with metrics
│   ├── crud.py                 # Database operations
│   ├── db.py                   # Database connection
│   ├── models.py               # SQLModel models
│   └── index.html              # Frontend interface
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Test fixtures
│   ├── test_health.py          # Health endpoint tests
│   └── test_todos.py           # CRUD operation tests
├── .dockerignore               # Docker ignore rules
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Docker Compose config
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── README.md                   # This file
└── REPORT.md                   # Assignment report
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server

### Testing
- **pytest** - Testing framework
- **pytest-cov** - Coverage measurement
- **httpx** - HTTP client for testing

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD automation
- **Google Cloud Run** - Serverless deployment
- **Prometheus Client** - Metrics collection

---

## 👨‍💻 Development Workflow

### Local Development

1. Activate virtual environment:
```bash
   source .venv/Scripts/activate  # Windows Git Bash
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
```

3. Run the app:
```bash
   uvicorn app.main:app --reload
```

4. Run tests:
```bash
   pytest
```

### Before Committing

Always run tests before committing:
```bash
pytest -v
```

Ensure coverage is above 70%

---

## 📚 API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve HTML frontend |
| GET | `/health` | Health check |
| GET | `/metrics` | Prometheus metrics |
| GET | `/todos` | List all todos |
| POST | `/todos` | Create a new todo |
| GET | `/todos/{id}` | Get a specific todo |
| PATCH | `/todos/{id}` | Update a todo |
| DELETE | `/todos/{id}` | Delete a todo |

---

## 🎓 Assignment Information

**Course:** Software Development and DevOps  
**Institution:** IE University  
**Assignment:** Individual Assignment 2  
**Student:** Jack Samawi  
**Date:** 15th of November 2025

---
