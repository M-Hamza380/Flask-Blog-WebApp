# Makefile

# Install dependencies
install:
		pip install -r requirements.txt

# Run the Flask application
run:
		python main.py

# Run tests using pytest
test:
		pytest tests/

# Format code using black
format:
		black src/ tests/

# Sort imports using isort
isort:
		isort src/ tests/ --verbose

# Lint code using flake8
lint:
		flake8 src/ tests/ --verbose

# clean pre-commit hooks
pre-commit-clean:
		pre-commit clean

# uninstall pre-commit hooks
pre-commit-uninstall:
		pre-commit uninstall

# install pre-commit hooks
pre-commit-install:
		pre-commit install

# run pre-commit hooks
pre-commit-run:
		pre-commit run --all-files

# Deploy using Gunicorn (for production)
deploy:
		gunicorn main:app

# Clean up .pyc files and caches
clean:
		find . -name "*.pyc" -exec rm -f {} \;
		find . -name "__pycache__" -exec rm -rf {} \;
