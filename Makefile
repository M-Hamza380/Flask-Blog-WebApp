# Makefile

# Install dependencies
install:
		pip install -r requirements.txt

# Run the Flask application
run:
		flask run

# Run tests using pytest
test:
		pytest

# Lint code using flake8
lint:
		flake8 src/

# Format code using black
format:
		black src/

# Sort imports using isort
isort:
		isort src/

# Run pre-commit hooks
pre-commit-install:
		pre-commit install

pre-commit-run:
		pre-commit run --all-files

# Deploy using Gunicorn (for production)
deploy:
		gunicorn main:app

# Clean up .pyc files and caches
clean:
		find . -name "*.pyc" -exec rm -f {} \;
		find . -name "__pycache__" -exec rm -rf {} \;
