# Project Management API Documentation

## Project Management Endpoints

### 1. Create Project

#### Endpoint

```
POST /projects/create
```

#### Body Input Example

```json
{
  "project_name": "Dashboard Redesign",
  "description": "UI/UX updates for the company dashboard.",
  "user_id": 1,
  "status": "In Progress"
}
```

#### Response Example

```json
{
  "status": 200,
  "message": "Project Created successfully",
  "project_id": 22
}
```

### 2. Get All Projects

#### Endpoint

```
GET /projects/user/:userId
```

#### Input Parameters

- `userId`: The ID of the user whose projects are being requested

#### Response Example

```json
[
  {
    "project_id": 22,
    "project_name": "Dashboard Redesign",
    "description": "UI/UX updates for the company dashboard.",
    "create_datetime": "2024-11-15 10:00:00",
    "update_datetime": "2024-11-18 14:00:00",
    "user_id": 1,
    "status": "In Progress"
  }
]
```

### 3. Update Project

#### Endpoint

```
POST /projects/update
```

#### Body Input Example

```json
{
  "project_id": 22,
  "project_name": "Dashboard Redesign",
  "description": "UI/UX updates for the company dashboard.",
  "status": "Completed"
}
```

#### Response Example

```json
{
  "status": 200,
  "message": "Project Updated successfully"
}
```

### 4. Delete Project

#### Endpoint

```
POST /projects/delete
```

#### Body Input Example

```json
{
  "project_id": 22
}
```

#### Response Example

```json
{
  "status": 200,
  "message": "Project deleted successfully"
}
```

### 5. View Project by ID

#### Endpoint

```
GET /projects/:project_id/user/:user_id
```

#### Input Parameters

- `project_id`: ID of the project to view
- `user_id`: ID of the user requesting the project details

#### Response Example

```json
{
  "project_id": 22,
  "project_name": "Dashboard Redesign",
  "description": "UI/UX updates for the company dashboard.",
  "create_datetime": "2024-11-15 10:00:00",
  "update_datetime": "2024-11-18 14:00:00",
  "user_id": 1,
  "team_members": [
    {
      "user_id": 1,
      "user_name": "john_doe",
      "is_owner": true
    }
  ],
  "tasks": [
    {
      "task_id": 201,
      "task_name": "Create wireframes",
      "description": "Design wireframes for the new dashboard layout.",
      "deadline": "2024-11-25 17:00:00",
      "priority": 1,
      "status": "In Progress",
      "tags": [
        {
          "tag_id": 1,
          "tag_name": "UI/UX"
        }
      ]
    }
  ]
}
```

## Task Management Endpoints

### 6. Create Task

#### Endpoint

```
POST /tasks/create
```

#### Body Input Example

```json
{
  "task_name": "Create wireframes",
  "description": "Design wireframes for the new dashboard layout.",
  "deadline": "2024-11-25 17:00:00",
  "priority": 1,
  "status": "In Progress",
  "project_id": 22,
  "assignee_id": 3
}
}
```

#### Response Example

```json
{
  "status": 200,
  "message": "Task created successfully",
  "task_id": 201
}
```

### 7. Update Task

#### Endpoint

```
POST /tasks/update
```

#### Body Input Example

```json
{
  "task_id": 201,
  "task_name": "Update wireframes",
  "description": "Adjust wireframes for the new dashboard layout.",
  "deadline": "2024-11-28 17:00:00",
  "priority": 2,
  "status": "In Progress",
  "assignee_id": 4
}
```

#### Response Example

```json
{
  "status": 200,
  "message": "Task updated successfully"
}
```

### 8. Delete Task

#### Endpoint

```
POST /tasks/delete
```

#### Body Input Example

```json
{
  "task_id": 201
}
```

#### Response Example

```json
{
  "status": 200,
  "message": "Task deleted successfully"
}
```

## Summary of Endpoints

### Projects

1. `POST /projects`: Create a new project
2. `GET /projects/user/:userId`: Retrieve all projects for a user
3. `POST /projects/update`: Update project details
4. `POST /projects/delete`: Delete a project
5. `GET /projects/:project_id/user/:user_id`: View detailed project information

### Tasks

6. `POST /tasks/create`: Create a new task
7. `POST /tasks/update`: Update task details
8. `POST /tasks/delete`: Delete a task
