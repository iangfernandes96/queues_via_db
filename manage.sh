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
    echo "  migrate             Run database migrations"
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
    docker compose up --build
    echo "Started Task Queue System"
    echo "API is running at http://localhost:8000"
    echo "API Documentation is available at http://localhost:8000/docs"
}

function stop {
    docker compose down
    echo "Stopped Task Queue System"
}

function restart {
    stop
    start
}

function logs {
    docker compose logs -f
}

function status {
    docker compose ps
}

function migrate {
    docker compose exec api alembic upgrade head
    echo "Database migrations applied"
}

function shell {
    docker compose exec api bash
}

function create_task {
    local name=$1
    local payload=$2
    local priority=$3
    local delay=$4

    if [ -z "$name" ]; then
        name="default_task"
    fi

    if [ -z "$payload" ]; then
        payload="{\"action\": \"print\", \"message\": \"Hello, World!\"}"
    fi

    if [ -z "$priority" ]; then
        priority=2
    fi

    # Build command args
    local cmd="python -m examples.submit_task --name $name --priority $priority"
    
    # Add delay if specified
    if [ -n "$delay" ]; then
        cmd="$cmd --delay $delay"
    fi
    
    # Add payload (careful with escaping)
    cmd="$cmd --payload '$payload'"
    
    # Execute in the API container
    docker compose exec api bash -c "$cmd"
}

function task_status {
    local task_id=$1
    
    if [ -z "$task_id" ]; then
        echo "Error: Task ID is required"
        exit 1
    fi
    
    curl -s http://localhost:8000/api/tasks/$task_id | python -m json.tool
}

function pause_task {
    local task_id=$1
    
    if [ -z "$task_id" ]; then
        echo "Error: Task ID is required"
        exit 1
    fi
    
    curl -s -X PATCH http://localhost:8000/api/tasks/$task_id/pause | python -m json.tool
}

function resume_task {
    local task_id=$1
    
    if [ -z "$task_id" ]; then
        echo "Error: Task ID is required"
        exit 1
    fi
    
    curl -s -X PATCH http://localhost:8000/api/tasks/$task_id/resume | python -m json.tool
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
        logs
        ;;
    status)
        status
        ;;
    migrate)
        migrate
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