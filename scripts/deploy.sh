#!/bin/bash
# Deployment script for AI Task Notify Hook

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="ai-task-notify-hook"
PROJECTS=("notify-tool" "notify-server" "notify-cli")

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check requirements
check_requirements() {
    log_info "Checking requirements..."

    if ! command -v uv &> /dev/null; then
        log_error "uv is not installed. Please install uv first."
        exit 1
    fi

    if ! command -v docker &> /dev/null; then
        log_warn "Docker is not installed. Docker deployment will be skipped."
        SKIP_DOCKER=true
    fi
}

# Run tests
run_tests() {
    log_info "Running tests..."
    uv run pytest test/ --cov=ai_task_notify_hook --cov-report=term-missing

    log_info "Running Polylith checks..."
    uv run poly check
}

# Build projects
build_projects() {
    log_info "Building projects..."

    # Clean previous builds
    rm -rf projects/*/dist/

    # Build all projects
    uv run poly build

    for project in "${PROJECTS[@]}"; do
        if [ -d "projects/$project" ]; then
            log_info "Building $project..."
            cd "projects/$project"
            uv build
            cd ../..
        fi
    done
}

# Build Docker images
build_docker_images() {
    if [ "$SKIP_DOCKER" = true ]; then
        log_warn "Skipping Docker build (Docker not available)"
        return
    fi

    log_info "Building Docker images..."

    # Build base image
    docker build -t "$PROJECT_NAME:latest" .

    # Build server image
    docker build --target server -t "$PROJECT_NAME-server:latest" .

    # Build CLI image
    docker build --target cli -t "$PROJECT_NAME-cli:latest" .
}

# Package for distribution
package_for_distribution() {
    log_info "Creating distribution packages..."

    # Create dist directory
    mkdir -p dist/

    # Copy all built wheels
    for project in "${PROJECTS[@]}"; do
        if [ -d "projects/$project/dist" ]; then
            cp projects/$project/dist/*.whl dist/
        fi
    done

    # Create source distribution
    tar -czf "dist/${PROJECT_NAME}-source.tar.gz" \
        --exclude='.git' \
        --exclude='__pycache__' \
        --exclude='.pytest_cache' \
        --exclude='htmlcov' \
        --exclude='*.pyc' \
        --exclude='dist' \
        --exclude='.venv' \
        .

    log_info "Distribution packages created in dist/"
}

# Deploy locally
deploy_local() {
    log_info "Deploying locally..."

    # Install all packages
    for project in "${PROJECTS[@]}"; do
        if [ -f "projects/$project/dist/"*.whl ]; then
            pip install --force-reinstall projects/$project/dist/*.whl
        fi
    done
}

# Deploy with Docker
deploy_docker() {
    if [ "$SKIP_DOCKER" = true ]; then
        log_warn "Skipping Docker deployment (Docker not available)"
        return
    fi

    log_info "Deploying with Docker..."
    docker-compose up -d notify-server
}

# Main deployment function
main() {
    log_info "Starting deployment for $PROJECT_NAME..."

    check_requirements
    run_tests
    build_projects
    build_docker_images
    package_for_distribution

    # Ask user for deployment method
    echo "Choose deployment method:"
    echo "1) Local installation"
    echo "2) Docker deployment"
    echo "3) Both"
    echo "4) Skip deployment"

    read -p "Enter your choice (1-4): " choice

    case $choice in
        1)
            deploy_local
            ;;
        2)
            deploy_docker
            ;;
        3)
            deploy_local
            deploy_docker
            ;;
        4)
            log_info "Skipping deployment"
            ;;
        *)
            log_error "Invalid choice"
            exit 1
            ;;
    esac

    log_info "Deployment completed successfully!"
}

# Run main function
main "$@"