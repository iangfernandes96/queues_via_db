# Task Queue System with PostgreSQL

A system that manages the execution of background tasks using PostgreSQL as a storage backend. The system consists of clients submitting tasks, a queue for storing these tasks, and workers processing them.

## Features

- **Delayed Job Support**: Schedule jobs to be executed at a future time
- **Job Status Lookup**: Query the status of jobs
- **Pause/Resume Jobs**: Ability to pause and resume jobs
- **Priority Support**: Assign different priority levels to jobs

## Architecture

The system is built with:
- **FastAPI**: For the REST API server
- **PostgreSQL 17**: As the storage backend
- **Docker**: For containerization

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository
2. Run the following command to start the system:

```bash
make up
```

The API will be available at http://localhost:8000.

### Usage

#### Submitting a Task

```bash
curl -X POST "http://localhost:8000/api/tasks/" \
     -H "Content-Type: application/json" \
     -d '{"name": "example_task", "payload": {"key": "value"}, "priority": "MEDIUM", "scheduled_at": "2023-10-01T10:00:00"}'
```

#### Getting Task Status

```bash
curl -X GET "http://localhost:8000/api/tasks/{task_uuid}"
```

#### Pausing a Task

```bash
curl -X PATCH "http://localhost:8000/api/tasks/{task_uuid}/pause"
```

#### Resuming a Task

```bash
curl -X PATCH "http://localhost:8000/api/tasks/{task_uuid}/resume"
```

## API Documentation

The API documentation is available at http://localhost:8000/docs when the system is running.

## Development

For developers working on this project:

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. Run linters and formatters:
   ```bash
   pre-commit run --all-files
   ```

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed instructions on:
- Setting up your development environment
- Using linters and formatters
- Running tests
- Contribution guidelines

## License

MIT

## Recent Updates

### UUID Implementation
- Task and Worker IDs are now UUIDs instead of integers, providing:
  - Better distributed system support
  - No ID collisions when scaling
  - Built-in creation timestamp information
  - Improved security by making IDs non-sequential
- All API endpoints now expect UUIDs in path parameters

### Timezone Handling
- All datetime fields are now consistently handled with timezone awareness
- Scheduled tasks correctly interpret the provided datetime
- Stored times include timezone information for accurate calculations
