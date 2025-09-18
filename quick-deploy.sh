#!/bin/bash

# Quick Deployment Script for Sentinel Project
# Deploy to Railway or Render in minutes

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
    echo -e "${BLUE}🚀 Sentinel Quick Deployment${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Check if we're in the right directory
check_directory() {
    if [ ! -f "sentinel_web_app_firebase.py" ]; then
        print_error "sentinel_web_app_firebase.py not found"
        print_error "Please run this script from the sentinel_package directory"
        exit 1
    fi
    print_status "Found Sentinel application files"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    print_status "Docker is running"
}

# Test local setup
test_local() {
    print_status "Testing local Docker setup..."
    
    # Build Docker image
    print_status "Building Docker image..."
    docker build -t sentinel-web-app:latest . > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        print_status "✅ Docker image built successfully"
    else
        print_error "❌ Docker build failed"
        exit 1
    fi
}

# Setup GitHub repository
setup_github() {
    print_status "Setting up GitHub repository..."
    
    # Check if git is initialized
    if [ ! -d ".git" ]; then
        print_status "Initializing git repository..."
        git init
    fi
    
    # Add all files
    git add .
    
    # Check if there are changes to commit
    if git diff --staged --quiet; then
        print_status "No changes to commit"
    else
        git commit -m "Initial Sentinel deployment"
        print_status "✅ Changes committed to git"
    fi
    
    # Check if remote exists
    if ! git remote get-url origin > /dev/null 2>&1; then
        print_warning "No GitHub remote configured"
        echo ""
        echo "Please create a GitHub repository:"
        echo "1. Go to https://github.com/new"
        echo "2. Create repository named 'sentinel-project'"
        echo "3. Copy the repository URL"
        echo ""
        read -p "Enter your GitHub repository URL: " REPO_URL
        
        if [ -n "$REPO_URL" ]; then
            git remote add origin "$REPO_URL"
            print_status "✅ GitHub remote added"
        else
            print_error "No repository URL provided"
            exit 1
        fi
    fi
    
    # Push to GitHub
    print_status "Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        print_status "✅ Code pushed to GitHub"
    else
        print_error "❌ Failed to push to GitHub"
        print_warning "Please check your GitHub credentials and repository URL"
        exit 1
    fi
}

# Deploy to Railway
deploy_railway() {
    print_status "Deploying to Railway..."
    
    # Check if Railway CLI is installed
    if ! command -v railway &> /dev/null; then
        print_status "Installing Railway CLI..."
        npm install -g @railway/cli
    fi
    
    # Login to Railway
    print_status "Please login to Railway..."
    railway login
    
    # Deploy
    print_status "Deploying to Railway..."
    railway up
    
    print_status "✅ Deployment to Railway complete!"
    print_status "Your app will be available at the URL provided by Railway"
}

# Deploy to Render
deploy_render() {
    print_status "Deploying to Render..."
    
    print_warning "Manual steps required for Render:"
    echo ""
    echo "1. Go to https://render.com"
    echo "2. Click 'New +' → 'Web Service'"
    echo "3. Connect your GitHub repository"
    echo "4. Use these settings:"
    echo "   - Environment: Docker"
    echo "   - Dockerfile Path: ./Dockerfile"
    echo "   - Start Command: streamlit run sentinel_web_app_firebase.py --server.port=\$PORT --server.address=0.0.0.0"
    echo "5. Click 'Create Web Service'"
    echo ""
    print_status "Render deployment guide provided!"
}

# Show deployment options
show_options() {
    print_header
    echo "Choose your deployment platform:"
    echo ""
    echo "1. Railway (Recommended - Easiest)"
    echo "   - Free tier: 500 hours/month"
    echo "   - Automatic deployments"
    echo "   - 5-minute setup"
    echo ""
    echo "2. Render"
    echo "   - Free tier: 750 hours/month"
    echo "   - Good performance"
    echo "   - Manual setup required"
    echo ""
    echo "3. Test local setup only"
    echo "   - Just test Docker build"
    echo "   - No cloud deployment"
    echo ""
}

# Main deployment function
main() {
    print_header
    
    # Check prerequisites
    check_directory
    check_docker
    
    # Show options
    show_options
    
    # Get user choice
    echo ""
    read -p "Choose option (1-3): " choice
    
    case $choice in
        1)
            test_local
            setup_github
            deploy_railway
            ;;
        2)
            test_local
            setup_github
            deploy_render
            ;;
        3)
            test_local
            print_status "Local setup test complete!"
            ;;
        *)
            print_error "Invalid choice. Please run the script again."
            exit 1
            ;;
    esac
    
    print_status "Deployment process completed!"
    echo ""
    print_status "Demo Credentials:"
    echo "  Police: police@saps.gov.za / police123"
    echo "  Bank: rep@standardbank.co.za / bank123"
    echo "  Security: security@adt.co.za / security123"
    echo "  Insurance: agent@santam.co.za / insurance123"
    echo ""
    print_status "Note: Police Officers and Bank Representatives have access to the Threat Map tab"
}

# Run main function
main "$@"
