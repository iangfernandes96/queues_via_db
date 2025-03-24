# Task Queue System API - Postman Collection Guide

This guide will help you set up and use the Postman collection for testing the Task Queue System API.

## Setting Up The Collection

1. Import the collection JSON file (`taskqueue-api.postman_collection.json`) into Postman
2. Create a new environment in Postman and set the following variables:
   - `baseUrl`: The base URL of your API (e.g., `http://localhost:8000`)

The collection includes automatic scripts to handle the following variables:
- `taskUuid`: Automatically captured when creating a task
- `scheduledTaskUuid`: Automatically captured when creating a scheduled task
- `workerUuid`: Automatically captured when creating a worker
- `workflow_task_id`: Used internally for workflow tests

## Collection Structure

The collection is organized into the following sections:

1. **Health Check**
   - API Health Check - Verifies the API is running

2. **Tasks**
   - Create Task - Submit a new task (automatically saves task UUID)
   - Create Scheduled Task - Submit a task with future execution time (automatically saves UUID)
   - List All Tasks - Get all tasks
   - Get Task by ID - Get details of a specific task
   - Update Task - Modify an existing task
   - Delete Task - Remove a task from the queue
   - Pause Task - Temporarily pause a task
   - Resume Task - Resume a paused task

3. **Workers**
   - Create Worker - Register a new worker (automatically saves worker UUID)
   - Get Worker by ID - Get worker details
   - Update Worker Heartbeat - Update worker heartbeat
   - Set Worker Status - Change worker status

4. **Task Workflow Test**
   - Series of requests to test the complete task lifecycle

## Using the Collection

### Testing Task Creation

1. Select the "Create Task" request
2. The request body should look like:
   ```json
   {
     "name": "sample_task",
     "payload": {
       "action": "print",
       "message": "Hello World"
     },
     "priority": "MEDIUM"
   }
   ```
3. Send the request
4. The response should contain the task details including a UUID
5. The UUID is automatically saved to the `taskUuid` environment variable

### Testing Task Status

1. Select the "Get Task by ID" request (no need to manually set the task UUID)
2. Send the request
3. You should see the details of the task, including its current status

### Creating a Worker

1. Select the "Create Worker" request
2. The request body should look like:
   ```json
   {
     "name": "worker-1"
   }
   ```
3. Send the request
4. The response should contain the worker details including a UUID
5. The UUID is automatically saved to the `workerUuid` environment variable

### Setting Worker Status

1. Select the "Set Worker Status" request (no need to manually set the worker UUID)
2. The request body should be:
   ```json
   {
     "status": "active"
   }
   ```
3. Send the request
4. You should see the updated worker details

## Advanced Testing

The collection includes a folder for "Task Workflow Test" that runs through a series of requests to test the entire task lifecycle. This includes:

1. Creating a new task
2. Checking its initial status
3. Updating the task
4. Pausing the task
5. Resuming the task
6. Deleting the task

To run this workflow, use Postman's Collection Runner feature.

## Troubleshooting

If you encounter errors:

1. Verify that the API server is running
2. Check that your environment variables are correctly set
3. Ensure the database is properly migrated and accessible
4. Check the API logs for detailed error messages

## Note on UUIDs

The system uses UUIDs instead of integers for task and worker IDs. These UUIDs are generated automatically when creating new resources. The Postman collection automatically captures these UUIDs and stores them in environment variables, so you don't need to manually copy them between requests. 