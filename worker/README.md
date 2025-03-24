# Worker Module

This module implements the worker component of the Task Queue System. Workers are responsible for picking up tasks from the queue and executing them.

## Features

- Polls the database for new tasks
- Executes tasks in order of priority
- Updates task status (running, completed, failed)
- Handles graceful shutdown on SIGTERM and SIGINT signals
- Maintains heartbeat to indicate worker health

## Configuration

The worker is configured using environment variables:

- `DATABASE_URL`: PostgreSQL connection string (required)
- `WORKER_POLL_INTERVAL`: How often to poll for new tasks in seconds (default: 5)
- `WORKER_MAX_TASKS`: Maximum number of tasks to process concurrently (default: 10)

## Running

Workers are typically run through Docker using the docker-compose.yml configuration. However, they can also be run directly:

```bash
python -m worker.main
```

## Scaling

To increase task processing capacity, you can increase the number of worker replicas in the docker-compose.yml file:

```yaml
deploy:
  replicas: 4  # Increase this number as needed
```
