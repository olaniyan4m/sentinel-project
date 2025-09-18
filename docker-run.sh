#!/bin/bash

# Sentinel Web Application Docker Runner
# This script provides easy commands to run the Sentinel project with Docker

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
    echo -e "${BLUE}🛡️  Sentinel Web Application${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Build the Docker image
build_image() {
    print_status "Building Sentinel Docker image..."
    docker build -t sentinel-web-app .
    print_status "Docker image built successfully!"
}

# Run with Docker Compose
run_compose() {
    print_status "Starting Sentinel with Docker Compose..."
    docker-compose up --build -d
    print_status "Sentinel is running!"
    print_status "Access the application at: http://localhost:8501"
}

# Run with Docker only
run_docker() {
    print_status "Starting Sentinel with Docker..."
    docker run -d \
        --name sentinel-web-app \
        -p 8501:8501 \
        -v "$(pwd)/real_data:/app/real_data" \
        -v "$(pwd)/logs:/app/logs" \
        sentinel-web-app
    print_status "Sentinel is running!"
    print_status "Access the application at: http://localhost:8501"
}

# Stop the application
stop_app() {
    print_status "Stopping Sentinel..."
    docker-compose down 2>/dev/null || docker stop sentinel-web-app 2>/dev/null || true
    docker rm sentinel-web-app 2>/dev/null || true
    print_status "Sentinel stopped!"
}

# Show logs
show_logs() {
    print_status "Showing Sentinel logs..."
    docker-compose logs -f sentinel-web-app 2>/dev/null || docker logs -f sentinel-web-app
}

# Show status
show_status() {
    print_status "Sentinel Status:"
    docker-compose ps 2>/dev/null || docker ps --filter "name=sentinel-web-app"
}

# Clean up
cleanup() {
    print_status "Cleaning up Sentinel containers and images..."
    docker-compose down -v 2>/dev/null || true
    docker stop sentinel-web-app 2>/dev/null || true
    docker rm sentinel-web-app 2>/dev/null || true
    docker rmi sentinel-web-app 2>/dev/null || true
    print_status "Cleanup complete!"
}

# Show help
show_help() {
    print_header
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build the Docker image"
    echo "  run       Run with Docker Compose (recommended)"
    echo "  docker    Run with Docker only"
    echo "  stop      Stop the application"
    echo "  logs      Show application logs"
    echo "  status    Show application status"
    echo "  cleanup   Clean up containers and images"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 run          # Start Sentinel with Docker Compose"
    echo "  $0 logs         # View application logs"
    echo "  $0 stop         # Stop the application"
    echo ""
    echo "Access URLs:"
    echo "  Web Application: http://localhost:8501"
    echo "  Landing Page: Open index.html in browser"
    echo ""
    echo "Demo Credentials:"
    echo "  Police: police@saps.gov.za / police123"
    echo "  Security: security@adt.co.za / security123"
    echo "  Insurance: agent@santam.co.za / insurance123"
    echo "  Bank: rep@standardbank.co.za / bank123"
}

# Main script logic
main() {
    print_header
    
    # Check Docker installation
    check_docker
    
    # Parse command
    case "${1:-help}" in
        "build")
            build_image
            ;;
        "run")
            build_image
            run_compose
            ;;
        "docker")
            build_image
            run_docker
            ;;
        "stop")
            stop_app
            ;;
        "logs")
            show_logs
            ;;
        "status")
            show_status
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@"
