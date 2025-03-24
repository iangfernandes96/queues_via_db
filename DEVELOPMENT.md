# Development Guide

This guide contains information for developers working on the Task Queue System project.

## Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/queues_via_db.git
   cd queues_via_db
   ```

2. Install the development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Code Quality Tools

This project uses several tools to ensure code quality:

### Pre-commit Hooks

Pre-commit hooks run automatically before each commit to ensure code quality. To run them manually:

```bash
pre-commit run --all-files
```

These hooks include:

- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with a newline
- **check-yaml/json**: Validates YAML and JSON files
- **debug-statements**: Catches debug statements (like pdb, ipdb)
- **detect-private-key**: Prevents committing private keys

### Code Formatters

- **Black**: The uncompromising Python code formatter
  ```bash
  black .
  ```

- **isort**: Sorts Python imports alphabetically
  ```bash
  isort .
  ```

### Linters

- **Flake8**: Style guide enforcement
  ```bash
  flake8
  ```

- **Mypy**: Static type checking
  ```bash
  mypy app worker tests
  ```

- **Pylint**: Code analysis
  ```bash
  pylint app worker
  ```

## Running Tests

Run tests using pytest:

```bash
pytest
```

For tests that use async functions:

```bash
pytest -xvs
```

## Managing Dependencies

- Main application dependencies are in `requirements.txt`
- Development dependencies are in `requirements-dev.txt`

When adding a new dependency:
1. Add it to the appropriate requirements file
2. Update your local environment: `pip install -r requirements-dev.txt`

## Pre-commit Configuration

The pre-commit hooks configuration is in `.pre-commit-config.yaml`. If you need to temporarily disable a hook for a specific commit:

```bash
SKIP=flake8,mypy git commit -m "Your commit message"
```

## CI/CD Integration

These linting tools are also run in the CI/CD pipeline, ensuring consistent code quality across the project.

## Pull Request Process

1. Ensure all tests pass locally before submitting a PR
2. Make sure pre-commit hooks pass without errors
3. Write meaningful commit messages
4. Add appropriate tests for new features 