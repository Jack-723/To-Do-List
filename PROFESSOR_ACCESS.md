# Professor Access Instructions

## Google Cloud Project Access

**Project ID:** `todo-list-devops`  
**Project Number:** `976425574918`  
**Region:** `europe-west1`

## Access Granted

You have been added as a **Viewer** to the Google Cloud project, giving you access to:
- Cloud Run services and deployment history
- Application logs and monitoring
- CI/CD pipeline configurations
- Service account details

## How to Access

1. Go to: https://console.cloud.google.com/
2. Switch to project: **todo-list-devops** (use the project selector at the top)
3. Navigate to **Cloud Run** to see the deployed service
4. View **Logs** and **Metrics** for the application

## Application URLs

**Live Application:** https://todo-list-app-976425574918.europe-west1.run.app/  
**Health Check:** https://todo-list-app-976425574918.europe-west1.run.app/health  
**Metrics (Prometheus):** https://todo-list-app-976425574918.europe-west1.run.app/metrics  
**API Documentation:** https://todo-list-app-976425574918.europe-west1.run.app/docs

## CI/CD Pipeline

**GitHub Actions:** https://github.com/Jack-723/To-Do-List/actions

The deployment is fully automated:
- Every push to `main` branch triggers the pipeline
- Tests run first, then Docker build, then automatic deployment
- Deployment takes approximately 3-4 minutes total

## Service Account

**Name:** `github-actions-deployer@todo-list-devops.iam.gserviceaccount.com`  
**Purpose:** Automated deployment from GitHub Actions  
**Permissions:** 
- Cloud Run Admin
- Service Account User
- Storage Admin
- Artifact Registry Writer
- Cloud Build Editor
- Service Usage Consumer

## Notes

- The application is publicly accessible (no authentication required)
- Data is ephemeral (SQLite in container - resets on scale-to-zero)
- Application scales automatically based on traffic
- Cold start time: ~1-2 seconds when idle