#!/usr/bin/env python
"""
Example script to submit a task to the Task Queue System.
"""
import argparse
import json
import sys
from datetime import datetime, timedelta

import httpx


def parse_args():
    parser = argparse.ArgumentParser(
        description="Submit a task to the Task Queue System"
    )
    parser.add_argument(
        "--name", type=str, default="example_task", help="Name of the task"
    )
    parser.add_argument(
        "--priority",
        type=int,
        default=2,
        choices=[1, 2, 3, 4],
        help="Priority of the task (1=LOW, 2=MEDIUM, 3=HIGH, 4=CRITICAL)",
    )
    parser.add_argument(
        "--payload",
        type=str,
        default='{"action": "print", "message": "Hello, World!"}',
        help="JSON payload for the task",
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=0,
        help="Delay in seconds before the task should be executed",
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default="http://localhost:8000/api",
        help="Base URL of the API",
    )
    return parser.parse_args()


def submit_task(args):
    api_url = f"{args.api_url}/tasks/"

    # Parse payload from string to JSON
    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON payload: {args.payload}")
        sys.exit(1)

    # Calculate scheduled time if delay is provided
    scheduled_at = None
    if args.delay > 0:
        scheduled_at = (datetime.utcnow() + timedelta(seconds=args.delay)).isoformat()

    # Prepare task data
    task_data = {
        "name": args.name,
        "payload": payload,
        "priority": args.priority,
    }

    if scheduled_at:
        task_data["scheduled_at"] = scheduled_at

    # Submit the task
    try:
        with httpx.Client() as client:
            response = client.post(api_url, json=task_data)
            response.raise_for_status()
            task = response.json()
            print(f"Task submitted successfully!")
            print(f"Task ID: {task['id']}")
            print(f"Status: {task['status']}")
            if scheduled_at:
                print(f"Scheduled at: {task['scheduled_at']}")
            print(f"To check the status: curl {args.api_url}/tasks/{task['id']}")

            return task["id"]
    except httpx.RequestError as e:
        print(f"Error submitting task: {e}")
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        print(
            f"Error submitting task: {e.response.status_code} {e.response.reason_phrase}"
        )
        print(f"Response: {e.response.text}")
        sys.exit(1)


def check_task_status(api_url, task_id):
    try:
        with httpx.Client() as client:
            response = client.get(f"{api_url}/tasks/{task_id}")
            response.raise_for_status()
            task = response.json()
            print(f"\nTask status: {task['status']}")
            if task["status"] == "completed":
                print(f"Result: {json.dumps(task['result'], indent=2)}")
            elif task["status"] == "failed":
                print(f"Error: {task['error']}")
            return task["status"]
    except httpx.RequestError as e:
        print(f"Error checking task status: {e}")
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        print(
            f"Error checking task status: {e.response.status_code} {e.response.reason_phrase}"
        )
        print(f"Response: {e.response.text}")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    task_id = submit_task(args)

    # If there's a delay, wait and check status
    if args.delay > 0:
        print(f"\nWaiting {args.delay} seconds for the task to complete...")
        import time

        time.sleep(args.delay + 5)  # Add a few extra seconds for processing
        check_task_status(args.api_url, task_id)
