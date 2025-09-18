#!/bin/bash

# Sentinel Cloud Deployment Script
# Deploy to multiple cloud platforms

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}🚀 Sentinel Cloud Deployment${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    print_status "Docker is running"
}

# Build Docker image
build_image() {
    print_status "Building Docker image for cloud deployment..."
    docker build -t sentinel-web-app:latest .
    print_status "Docker image built successfully!"
}

# Deploy to Railway (Recommended - Easiest)
deploy_railway() {
    print_status "Deploying to Railway..."
    
    # Check if Railway CLI is installed
    if ! command -v railway &> /dev/null; then
        print_warning "Railway CLI not found. Installing..."
        npm install -g @railway/cli
    fi
    
    # Login to Railway
    print_status "Please login to Railway..."
    railway login
    
    # Initialize project
    railway init
    
    # Deploy
    railway up
    
    print_status "Deployment to Railway complete!"
    print_status "Your app will be available at: https://your-app-name.railway.app"
}

# Deploy to Render
deploy_render() {
    print_status "Deploying to Render..."
    
    print_warning "Manual steps required for Render:"
    echo "1. Go to https://render.com"
    echo "2. Create a new Web Service"
    echo "3. Connect your GitHub repository"
    echo "4. Use the following settings:"
    echo "   - Environment: Docker"
    echo "   - Dockerfile Path: ./Dockerfile"
    echo "   - Start Command: streamlit run sentinel_web_app_firebase.py --server.port=\$PORT --server.address=0.0.0.0"
    echo "5. Add environment variables from render-deploy.yaml"
    
    print_status "Render deployment guide created!"
}

# Deploy to DigitalOcean
deploy_digitalocean() {
    print_status "Deploying to DigitalOcean..."
    
    print_warning "Manual steps required for DigitalOcean:"
    echo "1. Go to https://cloud.digitalocean.com/apps"
    echo "2. Create a new App"
    echo "3. Connect your GitHub repository"
    echo "4. Use the configuration from digitalocean-deploy.yml"
    echo "5. Deploy the app"
    
    print_status "DigitalOcean deployment guide created!"
}

# Deploy to Google Cloud
deploy_google_cloud() {
    print_status "Deploying to Google Cloud Run..."
    
    # Check if gcloud CLI is installed
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud CLI not found. Please install it first:"
        echo "https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    # Set project ID
    read -p "Enter your Google Cloud Project ID: " PROJECT_ID
    
    # Build and push to Google Container Registry
    print_status "Building and pushing to Google Container Registry..."
    docker tag sentinel-web-app:latest gcr.io/$PROJECT_ID/sentinel-web-app:latest
    docker push gcr.io/$PROJECT_ID/sentinel-web-app:latest
    
    # Deploy to Cloud Run
    print_status "Deploying to Cloud Run..."
    gcloud run deploy sentinel-web-app \
        --image gcr.io/$PROJECT_ID/sentinel-web-app:latest \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated \
        --port 8501 \
        --memory 1Gi \
        --cpu 1 \
        --max-instances 10
    
    print_status "Deployment to Google Cloud Run complete!"
}

# Deploy to AWS
deploy_aws() {
    print_status "Deploying to AWS ECS..."
    
    print_warning "AWS deployment requires additional setup:"
    echo "1. Install AWS CLI and configure credentials"
    echo "2. Create ECS cluster"
    echo "3. Push image to ECR"
    echo "4. Create task definition"
    echo "5. Create service"
    
    print_status "AWS deployment guide created!"
}

# Show deployment options
show_options() {
    print_header
    echo "Available deployment options:"
    echo ""
    echo "1. Railway (Recommended - Easiest)"
    echo "   - Free tier available"
    echo "   - Automatic deployments"
    echo "   - Easy setup"
    echo ""
    echo "2. Render"
    echo "   - Free tier available"
    echo "   - Good performance"
    echo "   - Manual setup required"
    echo ""
    echo "3. DigitalOcean App Platform"
    echo "   - $5/month minimum"
    echo "   - Good performance"
    echo "   - Manual setup required"
    echo ""
    echo "4. Google Cloud Run"
    echo "   - Pay-per-use"
    echo "   - Excellent performance"
    echo "   - Requires Google Cloud account"
    echo ""
    echo "5. AWS ECS/Fargate"
    echo "   - Pay-per-use"
    echo "   - Enterprise-grade"
    echo "   - Complex setup"
    echo ""
}

# Main deployment function
main() {
    print_header
    
    # Check Docker
    check_docker
    
    # Build image
    build_image
    
    # Show options
    show_options
    
    # Get user choice
    echo ""
    read -p "Choose deployment option (1-5): " choice
    
    case $choice in
        1)
            deploy_railway
            ;;
        2)
            deploy_render
            ;;
        3)
            deploy_digitalocean
            ;;
        4)
            deploy_google_cloud
            ;;
        5)
            deploy_aws
            ;;
        *)
            print_error "Invalid choice. Please run the script again."
            exit 1
            ;;
    esac
    
    print_status "Deployment process completed!"
    echo ""
    print_status "Next steps:"
    echo "1. Test your deployed application"
    echo "2. Set up custom domain (optional)"
    echo "3. Configure monitoring and alerts"
    echo "4. Set up CI/CD for automatic deployments"
}

# Run main function
main "$@"
