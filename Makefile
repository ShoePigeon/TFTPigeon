.PHONY: install init-db seed-db run test test-coverage

# Install dependencies
install:
	pip install -r requirements.txt

# Initialize the database
init-db:
	flask --app src init-db

# Seed data
seed-db:
	flask --app src seed-db

# Run the application
run:
	python run.py

# Run tests
test:
	python -m pytest

seed-db-email:
	flask --app src email-db

# Run tests with coverage
test-coverage:
	coverage run -m pytest
	coverage report