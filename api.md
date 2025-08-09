# Complete API Documentation

This document outlines all endpoints for the application.

## Table of Contents

- [Authentication](#authentication)
- [Dashboard](#dashboard)
- [Project](#project)
- [Task](#task)
- [Team](#team)

---

## Authentication

---

### Register User

**URL:** `/auth/register`  
**Method:** `POST`  
**Form Parameters:**

- `username` (required): User's username
- `email` (required): User's email address
- `password` (required): User's password
- `dob` (required): User's date of birth

**Response:**

- Success: Redirects to email validation page
- Error: Displays flash message with error

---

### Validate Email

**URL:** `/auth/validate-email`  
**Method:** `POST`  
**Form Parameters:**

- `email` (required): User's email address
- `code` (required): Validation code received via email

**Response:**

- Success: Redirects to login page
- Error: Displays flash message with error

---

### Login

**URL:** `/auth/login`  
**Method:** `POST`  
**Form Parameters:**

- `username` (required): User's username
- `password` (required): User's password

**Response:**

- Success: Redirects to index page with user session
- Error: Displays flash message with error

---

### Test Login (Development Only)

**URL:** `/auth/test-login`  
**Method:** `POST`  
**JSON Parameters:**

- `user_id` (required): User ID for test login

**Response:**

```json
{
  "message": "Test login successful"
}
```

---

### Logout

**URL:** `/auth/logout`  
**Method:** `GET`  
**Response:**

- Clears session and redirects to index page

**URL:** `/auth/dashboard`  
**Method:** `GET`  
**Authentication:** Required  
**Response:**

- Success: Renders dashboard template with user data
- Unauthorized: Redirects to login page

---

## Dashboard

---

### View Dashboard

**URL:** `/`  
**Method:** `GET`  
**Authentication:** Required  
**Response:**

- **Success:** Renders the dashboard template with user data (projects, teams, tasks).
- **Error:**
  - `400`: Missing required field `user_id` in session.
  - `404`: Error fetching projects for the user.

---

### View Calendar

**URL:** `/calendar`  
**Method:** `GET`  
**Authentication:** Required  
**Response:**

- **Success:** Renders the calendar view template with all tasks, showing their deadlines and associated projects.
- **Error:** Returns `500` error with the appropriate error message.

---

### Fetch All Tasks

**URL:** `/api/tasks`  
**Method:** `GET`  
**Authentication:** Required  
**Response:**

- **Success:** Returns a list of all tasks associated with the logged-in user’s projects.
- **Error:**
  - `500`: Error fetching tasks.

---

## Project

---

### Get Project Information

**URL:** `/project/info`  
**Method:** `GET`  
**Description:** Renders the project information page.

**Response:**

- **HTML Template:** `project/info.html`.

---

### List Projects

**URL:** `/project/list`  
**Method:** `GET`  
**Description:** Fetches all projects and renders them in the `list.html` template.

**Response:**

- **Success:**
  - **HTML Template:** `project/list.html`.
  - **Data:**
    - `projects`: List of user projects.
    - `teams`: List of teams for the user.
- **Error:** Renders the template with an empty list.

---

### Create Project Page

**URL:** `/project/create`  
**Method:** `GET`, `POST`  
**Description:**

- **GET:** Renders the project creation page with the user's teams.
- **POST:** Handles form submission for creating a project.

**Response:**

- **HTML Template:** `project/createProject.html`.
- **Data:**
  - `teams`: List of user's teams.

---

### Create Task Page

**URL:** `/project/create_task`  
**Method:** `GET`, `POST`  
**Description:**

- **GET:** Renders the task creation page.
- **POST:** Handles form submission for creating a task.

**Response:**

- **HTML Template:** `project/createTask.html`.

---

### Create Project

**URL:** `/project/create_project`  
**Method:** `POST`  
**Description:** Creates a new project for the logged-in user.

**Request Content-Type:**

- `application/json` or `application/x-www-form-urlencoded`

**Request Parameters:**

- `project_name` (required): Name of the project.
- `description` (required): Description of the project.
- `status` (optional): Project status (default: "Not Started").
- `team_ids` (optional): List of team IDs associated with the project.

**Response:**

- **Success:** Redirects to `/project/list`.
- **Error:** Returns a JSON response with error details.

---

### Create Project for Team

**URL:** `/project/<int:team_id>/create_project`  
**Method:** `POST`  
**Description:** Creates a project directly associated with a specific team.

**Request Parameters:**

- `project_name` (required): Name of the project.
- `description` (required): Description of the project.
- `status` (optional): Project status (default: "NOT STARTED").

**Response:**

- **Success:** Redirects to `/team/get/<team_id>`.
- **Error:** Displays a flash message with error details.

---

### Update Project

**URL:** `/project/update_project`  
**Method:** `POST`  
**Description:** Updates an existing project.

**Request Parameters:**

- `project_id` (required): ID of the project to be updated.
- `project_name` (required): Updated project name.
- `description` (required): Updated description.
- `status` (optional): Updated project status.

**Response:**

- **Success:** Displays a flash message indicating successful update.
- **Error:** Displays a flash message with error details.

---

### Delete Project

**URL:** `/project/delete_project`  
**Method:** `POST`  
**Description:** Deletes a project by its ID.

**Request Parameters:**

- `project_id` (required): ID of the project to delete.

**Response:**

- **Success:** Displays a flash message indicating successful deletion.
- **Error:** Displays a flash message with error details.

---

### Get Project Details

**URL:** `/project/get/<int:project_id>`  
**Method:** `GET`  
**Description:** Fetches details for a specific project, including tasks.

**Response:**

- **Success:**
  - **HTML Template:** `project/info.html`.
  - **Data:**
    - `project`: Project details.
    - `tasks_due_next_week`: Tasks grouped by day of the week for the next week.
- **Error:** Returns a JSON response with error details.

---

### Get Projects by User

**URL:** `/project/get_by_user`  
**Method:** `GET`  
**Description:** Fetches all projects associated with the logged-in user.

**Response:**

- **Success:**
  - **HTML Template:** `project/index.html`.
  - **Data:**
    - `projects`: List of user projects.
- **Error:** Returns a JSON response with error details.

---

## Task

---

### **Create Task**

**URL:** `/task/create`  
**Method:** `POST`  
**Description:** Creates a new task for a project.

**Request Content-Type:**

- `application/json` or `application/x-www-form-urlencoded`

  **Request Parameters:**

- **JSON Format:**
  - `task_name` (required): Name of the task.
  - `description` (optional): Description of the task.
  - `deadline` (optional): Deadline for the task (format: `YYYY-MM-DD`).
  - `priority` (optional): Priority level of the task.
  - `status` (optional): Current status of the task.
  - `assignee_id` (optional): ID of the user assigned to the task.
  - `project_id` (required): ID of the project the task belongs to.
- **Form Data Format:**

  - Same as above.

  **Response:**

- **Success:**
  - Flash message: "Task Added Successfully!"
  - Redirects to `/project/get/<project_id>`.
- **Error:**
  - **Status Code:** `400` or `415`
  - **Response:** JSON error message.

---

### **Update Task**

**URL:** `/task/update/`  
**Method:** `POST`  
**Description:** Updates an existing task.

**Request Parameters:**

- **JSON Format (for taskboard updates):**

  - `task_id` (required): ID of the task to update.
  - `project_id` (required): ID of the project the task belongs to.
  - `task_name` (optional): Updated task name.
  - `description` (optional): Updated task description.
  - `deadline` (optional): Updated deadline (format: `YYYY-MM-DD`).
  - `priority` (optional): Updated priority level.
  - `status` (optional): Updated status.
  - `assignee_id` (optional): Updated assignee ID.

- **Form Data Format:**

  - Same as above, but passed via form parameters.

  **Response:**

- **Success:**
  - Flash message: "Task Updated successfully!"
  - Redirects to `/project/get/<project_id>` for form requests.
  - JSON success message for taskboard updates.
- **Error:**
  - Flash message: "Task could not be updated."
  - Redirects to `/project/get/<project_id>`.

---

### **Delete Task**

**URL:** `/task/delete/<int:task_id>`  
**Method:** `POST`  
**Description:** Deletes a task by its ID.

**Response:**

- **Success:**
  - Flash message: "Task Deleted successfully!"
  - Redirects to `/project/get/<project_id>`.
- **Error:**
  - **Status Code:** `404`
  - **Response:** JSON error message.

---

### **Taskboard View**

**URL:** `/task/project/<int:project_id>/taskboard`  
**Method:** `GET`  
**Description:** Displays the taskboard for a specific project, showing its tasks.

**Response:**

- **Success:**
  - Renders `task/TaskBoard.html`.
  - **Data Passed to Template:**
    - `project_name`: Name of the project.
    - `tasks`: List of tasks for the project.
    - `project_id`: ID of the project.
- **Error:**
  - Renders `error.html` with an error message if the project is not found.

---

# Team

---

### List Teams

**URL:** `/team/list`  
**Method:** `GET`  
**Description:** Fetches the list of teams associated with the logged-in user.

**Response:**

- **Success:**
  - Renders `team/list.html`.
  - **Data Passed to Template:**
    - `teams`: List of user's teams.
    - `users`: List of all users.
    - `owner`: ID of the logged-in user.
- **Error:**
  - **Status Code:** `500`
  - **Response:** JSON error message.

---

### **Create Team**

**URL:** `/team/create`  
**Method:** `POST`  
**Description:** Creates a new team with specified details.

**Request Parameters:**

- `team_name` (required): Name of the team.
- `description` (optional): Description of the team.
- `assignees` (optional): List of user IDs to be added as team members.

  **Response:**

- **Success:**
  - Redirects to `/team/list`.
- **Error:**
  - **Status Code:** `500`
  - **Response:** JSON error message.

---

### **Update Team**

**URL:** `/team/update`  
**Method:** `POST`  
**Description:** Updates details of an existing team.

**Request Parameters:**

- `team_id` (required): ID of the team to update.
- `team_name` (required): Updated name of the team.
- `description` (optional): Updated description of the team.
- `assignees` (optional): Updated list of user IDs.
- `owner_id` (optional): Updated owner ID.

  **Response:**

- **Success:**
  - Redirects to `/team/list`.
- **Error:**
  - **Status Code:** `500`
  - **Response:** JSON error message.

---

### **Delete Team**

**URL:** `/team/delete/<int:team_id>`  
**Method:** `POST`  
**Description:** Deletes a team by its ID.

**Response:**

- **Success:**
  - Redirects to `/team/list`.
- **Error:**
  - **Status Code:** `404`
  - **Response:** JSON error message.

---

### **Get Team Details**

**URL:** `/team/get/<int:team_id>/`  
**Method:** `GET`  
**Description:** Fetches details of a team, including associated projects and members.

**Response:**

- **Success:**
  - Renders `team/info.html`.
  - **Data Passed to Template:**
    - `projects`: List of projects associated with the team.
    - `team`: Team details.
    - `users`: List of all users.
- **Error:**
  - **Status Code:** `404`
  - **Response:** JSON error message.

---

### **Add Member to Team**

**URL:** `/team/add/member`  
**Method:** `POST`  
**Description:** Adds a new member to a team with a specified role.

**Request Parameters:**

- `team_id` (required): ID of the team.
- `member_name` (required): ID of the user to add as a member.
- `is_owner` (optional): Role of the user (0 = Member, 1 = Owner).

  **Response:**

- **Success:**
  - Flash message: "Member added successfully!"
  - Redirects to `/team/get/<team_id>`.
- **Error:**
  - Flash message with error details.
  - Redirects to the referring page.

---

### **Delete Member from Team**

**URL:** `/team/delete/member`  
**Method:** `POST`  
**Description:** Removes a member from a team.

**Request Parameters:**

- `team_id` (required): ID of the team.
- `member_id` (required): ID of the user to remove.

  **Response:**

- **Success:**
  - Flash message: "Member removed successfully!"
  - Redirects to `/team/get/<team_id>`.
- **Error:**
  - Flash message with error details.
  - Redirects to the referring page.

---

## Additional Information

**Authentication**

- All routes require session-based authentication
- User ID must be present in the session
- Unauthorized access redirects to login page

**Date Handling**

- Project tasks use datetime format: "YYYY-MM-DD HH:MM:SS"
- Week calculations start from Sunday
- Task deadlines are adjusted by adding one day

**Error Handling**

- All routes include try-catch blocks for error handling
- Errors are returned with appropriate HTTP status codes
- Flash messages are used for user feedback
- Redirects maintain user context on errors
