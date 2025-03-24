#!/bin/bash

# Simple management script for the Task Queue System

set -e

function show_help {
    echo "Usage: $0 <command>"
    echo ""
    echo "Commands:"
    echo "  start               Start the Task Queue System"
    echo "  stop                Stop the Task Queue System"
    echo "  restart             Restart the Task Queue System"
    echo "  logs                Show logs (Ctrl+C to exit)"
    echo "  status              Show the status of all containers"
    echo "  migrate             Run database migrations (requires API container)"
    echo "  direct-migrate      Run migrations directly (doesn't require API container)"
    echo "  migration-status    Check current migration status (doesn't require API container)"
    echo "  shell               Open a shell in the API container"
    echo "  create-task <name>  Create a task with the given name"
    echo "  task-status <id>    Check the status of a task"
    echo "  pause-task <id>     Pause a task"
    echo "  resume-task <id>    Resume a paused task"
    echo "  help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 create-task my_task '{\"key\": \"value\"}' 3"
    echo "  $0 task-status 1"
}

function start {
    echo "Starting Task Queue System..."
    docker compose up --build -d
    echo "System started. API available at http://localhost:8000"
}

function stop {
    echo "Stopping Task Queue System..."
    docker compose down
    echo "System stopped."
}

function restart {
    stop
    start
}

function logs {
    local service=$1
    if [ -z "$service" ]; then
        docker compose logs -f
    else
        docker compose logs -f "$service"
    fi
}

function status {
    docker compose ps
}

function migrate {
    echo "Running database migrations..."
    docker compose exec api alembic upgrade head
    echo "Migrations complete."
}

function direct_migrate {
    echo "Running database migrations directly against the database..."

    # Check if postgres container is running
    if ! docker compose ps | grep -q "postgres.*running"; then
        echo "Starting postgres container..."
        docker compose up -d postgres
        # Wait for postgres to be ready
        echo "Waiting for postgres to be ready..."
        sleep 5
    fi

    # Create a temporary container that connects to the Postgres network
    # and runs alembic migrations directly
    docker run --rm \
        --network queues_via_db_default \
        -v "$(pwd):/app" \
        -w /app \
        -e DATABASE_URL=postgresql://postgres:postgres@postgres:5432/taskqueue \
        python:3.11-slim \
        bash -c "pip install -r requirements.txt && PYTHONPATH=. alembic upgrade head"
    echo "Direct migrations complete."
}

function migration_status {
    echo "Checking migration status..."

    # Check if postgres container is running
    if ! docker compose ps | grep -q "postgres.*running"; then
        echo "Starting postgres container..."
        docker compose up -d postgres
        # Wait for postgres to be ready
        echo "Waiting for postgres to be ready..."
        sleep 5
    fi

    # Create a temporary container that connects to the Postgres network
    # and runs alembic current command to show migration status
    docker run --rm \
        --network queues_via_db_default \
        -v "$(pwd):/app" \
        -w /app \
        -e DATABASE_URL=postgresql://postgres:postgres@postgres:5432/taskqueue \
        python:3.11-slim \
        bash -c "pip install -r requirements.txt && PYTHONPATH=. alembic current"
}

function shell {
    docker compose exec api /bin/bash
}

function create_task {
    local name=$1
    local payload=$2
    local priority=${3:-"MEDIUM"}
    local scheduled_at=$4

    if [ -z "$name" ] || [ -z "$payload" ]; then
        echo "Usage: $0 create-task <name> <payload_json> [priority] [scheduled_at]"
        echo "Example: $0 create-task \"my_task\" '{\"action\":\"print\",\"message\":\"Hello, World!\"}' \"HIGH\" \"2023-10-01T12:00:00\""
        exit 1
    fi

    # Build JSON request body
    local request_body
    if [ -z "$scheduled_at" ]; then
        request_body="{\"name\":\"$name\",\"payload\":$payload,\"priority\":\"$priority\"}"
    else
        request_body="{\"name\":\"$name\",\"payload\":$payload,\"priority\":\"$priority\",\"scheduled_at\":\"$scheduled_at\"}"
    fi

    # Make API call
    echo "Creating task with name: $name"
    echo "Request body: $request_body"

    curl -s -X POST -H "Content-Type: application/json" -d "$request_body" http://localhost:8000/api/tasks | jq .
}

function task_status {
    local task_id=$1

    if [ -z "$task_id" ]; then
        echo "Usage: $0 task-status <task_uuid>"
        echo "Example: $0 task-status 123e4567-e89b-12d3-a456-426614174000"
        exit 1
    fi

    echo "Getting status for task with UUID: $task_id"
    curl -s -X GET http://localhost:8000/api/tasks/$task_id | jq .
}

function pause_task {
    local task_id=$1

    if [ -z "$task_id" ]; then
        echo "Usage: $0 pause-task <task_uuid>"
        echo "Example: $0 pause-task 123e4567-e89b-12d3-a456-426614174000"
        exit 1
    fi

    echo "Pausing task with UUID: $task_id"
    curl -s -X POST http://localhost:8000/api/tasks/$task_id/pause | jq .
}

function resume_task {
    local task_id=$1

    if [ -z "$task_id" ]; then
        echo "Usage: $0 resume-task <task_uuid>"
        echo "Example: $0 resume-task 123e4567-e89b-12d3-a456-426614174000"
        exit 1
    fi

    echo "Resuming task with UUID: $task_id"
    curl -s -X POST http://localhost:8000/api/tasks/$task_id/resume | jq .
}

# Check if command was provided
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

# Parse command
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs "$2"
        ;;
    status)
        status
        ;;
    migrate)
        migrate
        ;;
    direct-migrate)
        direct_migrate
        ;;
    migration-status)
        migration_status
        ;;
    shell)
        shell
        ;;
    create-task)
        create_task "$2" "$3" "$4" "$5"
        ;;
    task-status)
        task_status "$2"
        ;;
    pause-task)
        pause_task "$2"
        ;;
    resume-task)
        resume_task "$2"
        ;;
    help)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
