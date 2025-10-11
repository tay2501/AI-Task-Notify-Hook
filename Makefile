.PHONY: help install test lint format check build docs clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync --dev

test: ## Run tests
	uv run pytest test/ --cov=ai_task_notify_hook --cov-report=term-missing

test-verbose: ## Run tests with verbose output
	uv run pytest test/ -v --cov=ai_task_notify_hook --cov-report=term-missing --cov-report=html

lint: ## Run linting checks
	uv run ruff check components/ bases/ test/
	uv run mypy components/ bases/ --ignore-missing-imports

format: ## Format code
	uv run ruff format components/ bases/ test/
	uv run isort components/ bases/ test/

format-check: ## Check code formatting
	uv run ruff format --check components/ bases/ test/

check: ## Run all checks (lint, format, test)
	$(MAKE) lint
	$(MAKE) format-check
	$(MAKE) test
	uv run poly check

poly-check: ## Validate Polylith workspace
	uv run poly check

poly-test: ## Run Polylith-based tests
	uv run poly test

build: ## Build all projects
	uv run poly build
	cd projects/notify-tool && uv build

docs: ## Build documentation
	cd docs && uv run sphinx-build -b html source build/html

docs-serve: ## Serve documentation locally
	cd docs && uv run python -m http.server 8000 --directory build/html

clean: ## Clean build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/
	rm -rf docs/build/
	rm -rf projects/*/dist/
	rm -rf projects/*/build/

setup-dev: ## Set up development environment
	uv sync --dev
	uv run pre-commit install

update: ## Update dependencies
	uv sync --upgrade

release: ## Prepare release
	$(MAKE) clean
	$(MAKE) check
	$(MAKE) build

# CI/CD helpers
ci-test: ## Run CI tests
	uv run pytest test/ --cov=ai_task_notify_hook --cov-report=xml

ci-build: ## Build for CI
	uv run poly build
	cd projects/notify-tool && uv build