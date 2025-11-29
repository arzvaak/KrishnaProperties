# Deployment Script for Krishna Real Estate
$ErrorActionPreference = "Stop"

$PROJECT_ID = "krishna-properties-f396d"
$REGION = "asia-south1"
$BACKEND_SERVICE = "krishna-backend"

Write-Host "Starting Deployment..." -ForegroundColor Green

# 1. Build and Deploy Backend to Cloud Run
Write-Host "`n[1/3] Deploying Backend to Cloud Run..." -ForegroundColor Cyan
Set-Location backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/$BACKEND_SERVICE --project $PROJECT_ID
gcloud run deploy $BACKEND_SERVICE `
    --image gcr.io/$PROJECT_ID/$BACKEND_SERVICE `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --project $PROJECT_ID `
    --set-env-vars "FLASK_DEBUG=False"
Set-Location ..

# 2. Build Frontend
Write-Host "`n[2/3] Building Frontend..." -ForegroundColor Cyan
Set-Location frontend
$env:VITE_API_URL = "https://krishna-backend-893324822718.asia-south1.run.app"
npm run build
Set-Location ..

# 3. Deploy to Firebase Hosting
Write-Host "`n[3/3] Deploying to Firebase Hosting..." -ForegroundColor Cyan
firebase deploy --only hosting --project $PROJECT_ID

Write-Host "`nDeployment Complete!" -ForegroundColor Green
