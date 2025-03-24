# Task Queue System - Postman Collection Guide

This guide explains how to use the Postman collection to test the Task Queue System API.

## Getting Started

1. **Import the Collection**
   - Open Postman
   - Click "Import" in the top left
   - Select the `taskqueue-api.postman_collection.json` file
   - The collection will be imported with all requests

2. **Set Environment Variables (Optional)**
   - Create a new Environment in Postman (click the gear icon ⚙️)
   - Add a variable named `baseUrl` with the value `http://localhost:8000` (or your API URL)
   - Select this environment from the dropdown in the top right

## Collection Structure

The collection is organized into three main folders:

1. **Health Check**
   - Basic endpoint to verify the API is running

2. **Tasks**
   - Create Task - Create a new task
   - Create Scheduled Task - Create a task scheduled for future execution
   - Get All Tasks - List tasks with pagination
   - Get Task by ID - Get a specific task
   - Update Task - Update task details
   - Delete Task - Delete a task
   - Pause Task - Pause a pending/running task
   - Resume Task - Resume a paused task
   - Get Pending Tasks - Filter tasks by pending status
   - Get Completed Tasks - Filter tasks by completed status

3. **Workers**
   - Create Worker - Register a new worker
   - Get Worker by ID - Get worker details
   - Update Worker Heartbeat - Update worker heartbeat
   - Set Worker Status - Change worker status

4. **Task Workflow Tests**
   - Create and Track Task - Test the full lifecycle of a task
     - 1. Create Task
     - 2. Check Task Status
     - 3. Pause Task
     - 4. Resume Task
     - 5. Delete Task

## Running Tests

### Individual Requests

1. Open a request from the collection
2. Modify the request body if needed
3. Click "Send" to execute the request
4. View the response in the lower panel

### Workflow Tests

The collection includes a workflow test that creates, manipulates, and deletes a task:

1. In Postman, click on the "Task Workflow Tests" folder
2. Click the "▶️ Run" button
3. A runner will open with all requests in the workflow selected
4. Click "Run Task Workflow Tests" to execute the entire sequence
5. The tests will run in order, creating a task and then performing operations on it

## Request Bodies

### Creating a Task
```json
{
  "name": "example_task",
  "payload": {
    "action": "print",
    "message": "Hello, World!"
  },
  "priority": 2,
  "scheduled_at": null
}
```

### Creating a Scheduled Task
```json
{
  "name": "scheduled_task",
  "payload": {
    "action": "process",
    "data": "This is a scheduled task"
  },
  "priority": 3,
  "scheduled_at": "2023-10-01T10:00:00"
}
```

### Updating a Task
```json
{
  "name": "updated_task_name",
  "payload": {
    "action": "print",
    "message": "Updated message"
  },
  "priority": 4
}
```

### Creating a Worker
```json
{
  "name": "worker-1"
}
```

### Setting Worker Status
```json
{
  "status": "inactive"
}
```

## Tips

- The Workflow Tests use Postman's variable system to store and reuse the task ID
- You can view the test scripts by clicking on the "Tests" tab in each request in the workflow
- All requests use the `{{baseUrl}}` variable, so make sure your environment is set correctly
- Use the collection runner (click on the folder and then "Run") to execute a sequence of requests 