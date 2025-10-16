TFTPigeon

## About TFT Pigeon

**TFT Pigeon** is a powerful and user friendly application designed to streamline development workflows, improve collaboration, and enhance productivity.

## Overview

TFT Pigeon is a collaborative project management tool designed to streamline team coordination and task management. It includes features like team and project organization, task tracking, and email-based notification systems for deadlines. The dashboard also integrates a calendar view for a comprehensive overview of upcoming tasks.
Based on a group project I did with Team Ate, currently adding features to support TFT game play and analysis.


## Key Features

### User Account Management

- **Create Account:** Users can create an account with email verification using a one-time code.
- **Login:** After verifying their email, users can log in to access the dashboard.
- **Logout:** Users can log out by clicking the button in the top-right corner.

### Team Management

- Create teams with:
  - Team name
  - Description
  - Team owner
  - Assignees
- View and edit all teams.

### Project Management

- Within each team, create projects with:
  - Project name
  - Description
  - Status 
- Switch to a **Taskboard View** for projects to organize tasks by their status:
  - Not Started
  - In Progress
  - Completed
  - Cancelled

### Task Management

- For each project, add tasks with:
  - Task name
  - Description
  - Deadline
  - Priority
  - Status
  - Assignees
- View and edit tasks directly in the Project Hub.

### Calendar Integration

- A calendar displays tasks across all teams and projects.
- Clicking on a date shows tasks with deadlines on that day.

### Notifications

- Email reminders:
  - Daily emails for all tasks with deadlines in the next 7 days.
  - Specific task reminders for deadlines within 24 hours.

### TFT Game History

- Game History:
	- View Previous Game history
	- Save Games played (IN PROGRESS)

---

## How to Run and Test

1. Install dependencies:
   ```bash
   make install
   ```
2. Initialize the database:
   ```bash
   make init-db
   ```
3. Start the application and register your email:
   ```bash
   make run
   ```
4. Seed the database with test emails:
   ```bash
   make seed-db-email
   ```
5. Run the application:
   ```bash
   make run
   ```

---
