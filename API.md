# Task Queue System API Documentation

This document provides details on how to use the Task Queue System API.

## Base URL

All API endpoints are prefixed with `/api`. For local development, the full URL would be:

```
http://localhost:8000/api
```

## Authentication

Currently, the API does not require authentication.

## Endpoints

### Tasks

#### Create a Task

Create a new task to be processed by the workers.

- **URL**: `/tasks/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "name": "example_task",
    "payload": {
      "key": "value"
    },
    "priority": 2,
    "scheduled_at": "2023-10-01T10:00:00"
  }
  ```
  - `name`: String, required - Name of the task
  - `payload`: Object, required - Data needed to process the task
  - `priority`: Integer, optional (default=2) - Priority (1=LOW, 2=MEDIUM, 3=HIGH, 4=CRITICAL)
  - `scheduled_at`: ISO8601 DateTime, optional - When to execute the task (if null, immediate execution)

- **Success Response**:
  - **Code**: 201 Created
  - **Content**:
    ```json
    {
      "id": 1,
      "name": "example_task",
      "payload": {
        "key": "value"
      },
      "priority": 2,
      "scheduled_at": "2023-10-01T10:00:00",
      "status": "scheduled",
      "created_at": "2023-09-28T15:30:00",
      "updated_at": "2023-09-28T15:30:00",
      "started_at": null,
      "completed_at": null,
      "worker_id": null,
      "result": null,
      "error": null
    }
    ```

#### Get All Tasks

Retrieve a list of all tasks.

- **URL**: `/tasks/`
- **Method**: `GET`
- **Query Parameters**:
  - `skip`: Integer, optional (default=0) - Number of records to skip
  - `limit`: Integer, optional (default=100) - Maximum number of records to return
  - `status`: String, optional - Filter by status (e.g., "pending", "running", "completed")

- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Array of task objects

#### Get a Task

Retrieve a specific task by ID.

- **URL**: `/tasks/{task_id}`
- **Method**: `GET`
- **URL Parameters**:
  - `task_id`: Integer, required - ID of the task

- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Task object

- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"detail": "Task not found"}`

#### Update a Task

Update a specific task.

- **URL**: `/tasks/{task_id}`
- **Method**: `PUT`
- **URL Parameters**:
  - `task_id`: Integer, required - ID of the task
- **Request Body**: Same as Create Task, but all fields are optional

- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Updated task object

- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"detail": "Task not found"}`

#### Delete a Task

Delete a specific task.

- **URL**: `/tasks/{task_id}`
- **Method**: `DELETE`
- **URL Parameters**:
  - `task_id`: Integer, required - ID of the task

- **Success Response**:
  - **Code**: 204 No Content

- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"detail": "Task not found"}`

#### Pause a Task

Pause a running or pending task.

- **URL**: `/tasks/{task_id}/pause`
- **Method**: `PATCH`
- **URL Parameters**:
  - `task_id`: Integer, required - ID of the task

- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Updated task object with status "paused"

- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"detail": "Task not found or cannot be paused (must be in PENDING, SCHEDULED, or RUNNING state)"}`

#### Resume a Task

Resume a paused task.

- **URL**: `/tasks/{task_id}/resume`
- **Method**: `PATCH`
- **URL Parameters**:
  - `task_id`: Integer, required - ID of the task

- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Updated task object with status "pending" or "scheduled"

- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"detail": "Task not found or cannot be resumed (must be in PAUSED state)"}`

### Workers

#### Create a Worker

Register a new worker.

- **URL**: `/workers/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "name": "worker-1"
  }
  ```
  - `name`: String, required - Name of the worker

- **Success Response**:
  - **Code**: 201 Created
  - **Content**:
    ```json
    {
      "id": 1,
      "name": "worker-1",
      "status": "active",
      "last_heartbeat": "2023-09-28T15:30:00",
      "created_at": "2023-09-28T15:30:00",
      "updated_at": "2023-09-28T15:30:00"
    }
    ```

#### Get a Worker

Retrieve worker information.

- **URL**: `/workers/{worker_id}`
- **Method**: `GET`
- **URL Parameters**:
  - `worker_id`: Integer, required - ID of the worker

- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Worker object

- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"detail": "Worker not found"}`

#### Update Worker Heartbeat

Update the heartbeat timestamp of a worker.

- **URL**: `/workers/{worker_id}/heartbeat`
- **Method**: `PATCH`
- **URL Parameters**:
  - `worker_id`: Integer, required - ID of the worker

- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Updated worker object

- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"detail": "Worker not found"}`

#### Set Worker Status

Update the status of a worker.

- **URL**: `/workers/{worker_id}/status`
- **Method**: `PATCH`
- **URL Parameters**:
  - `worker_id`: Integer, required - ID of the worker
- **Request Body**:
  ```json
  {
    "status": "inactive"
  }
  ```
  - `status`: String, required - New status for the worker

- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Updated worker object

- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"detail": "Worker not found"}`

## Task Status Values

- `pending`: Task is in the queue waiting to be processed
- `scheduled`: Task is scheduled for future execution
- `running`: Task is currently being processed by a worker
- `paused`: Task is paused and won't be processed until resumed
- `completed`: Task has been successfully completed
- `failed`: Task processing failed

## Task Priority Values

- `1`: LOW
- `2`: MEDIUM (default)
- `3`: HIGH
- `4`: CRITICAL
