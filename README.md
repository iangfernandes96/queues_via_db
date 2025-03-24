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
     -d '{"name": "example_task", "payload": {"key": "value"}, "priority": 1, "scheduled_at": "2023-10-01T10:00:00"}'
```

#### Getting Task Status

```bash
curl -X GET "http://localhost:8000/api/tasks/{task_id}"
```

#### Pausing a Task

```bash
curl -X PATCH "http://localhost:8000/api/tasks/{task_id}/pause"
```

#### Resuming a Task

```bash
curl -X PATCH "http://localhost:8000/api/tasks/{task_id}/resume"
```

## API Documentation

The API documentation is available at http://localhost:8000/docs when the system is running.

## License

MIT 