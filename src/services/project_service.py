from src.models.db import get_db

def get_project_by_id(project_id):
    """Get project data using project_id, along with team members and tasks."""
    db = get_db()

    try:
        # Fetch project data
        project_query = """
        SELECT 
            p.project_id,
            p.project_name,
            p.description,
            p.create_datetime,
            p.update_datetime,
            p.user_id AS project_owner_id,
            p.status
        FROM Project p
        WHERE p.project_id = ?
        """
        project = db.execute(project_query, (project_id,)).fetchone()
        print('Project fetch successful')

        if project is None:
            return None, "Project not found."

        # Fetch team members for this project
        team_members_query = """
        SELECT 
            tm.user_id,
            u.user_name AS team_member_name
        FROM Team_Members tm
        LEFT JOIN User u ON tm.user_id = u.user_id
        LEFT JOIN Project_Teams pt ON tm.team_id = pt.team_id
        WHERE pt.project_id = ?
        """
        team_members = db.execute(team_members_query, (project_id,)).fetchall()
        print('Team members fetch successful')

        # Fetch tasks for this project
        tasks_query = """
        SELECT 
            t.task_id,
            t.task_name,
            t.deadline,
            t.status,
            t.priority,
            t.assignee_id,
            t.description
        FROM Task t
        WHERE t.project_id = ?
        """
        tasks = db.execute(tasks_query, (project_id,)).fetchall()
        print('Tasks fetch successful')

        # Convert project result into a dictionary
        project_dict = {
            "project_id": project["project_id"],
            "project_name": project["project_name"],
            "description": project["description"],
            "create_datetime": project["create_datetime"],
            "update_datetime": project["update_datetime"],
            "project_owner_id": project["project_owner_id"],
            "status": project["status"],
            "team_members": [
                {"user_id": member["user_id"], "name": member["team_member_name"]}
                for member in team_members
            ],
            "tasks": [
                {"task_id": task["task_id"], "task_name": task["task_name"], "deadline": task["deadline"],"status":task["status"],"priority":task["priority"],
             "assignee_id": task["assignee_id"],"description":task['description']}
                for task in tasks
            ]
        }
        print(project_dict)
        return project_dict, None

    except Exception as e:
        print(f"Error fetching project data: {e}")
        return None, "An error occurred while fetching project data."

def get_projects_by_user_id(user_id):
    """Get project data using project_id"""
    db = get_db()
    print("before team name")
    projects = db.execute(
        """WITH team1  as(
        SELECT Team_Members.team_id,team_name FROM Team_Members left join Team  on Team_Members.team_id = Team.team_id where user_id = ? 
        ),
        list_projects as (
        SELECT project_id, team1.team_name FROM Project_Teams inner join team1 on team1.team_id = Project_Teams.team_id
        )
        SELECT 
        p.project_id,
        p.project_name,
        p.description, 
        p.create_datetime, 
        p.update_datetime, 
        p.user_id, p.status,
        m.team_name
        FROM 
        Project p 
        INNER JOIN
        list_projects m 
        on p.project_id = m.project_id
        """, (user_id,)
    ).fetchall()
    print("printing team name")
    print(projects)
    tasks_query = """
        SELECT 
            t.task_id,
            t.task_name,
            t.deadline,
            t.status,
            t.priority,
            t.assignee_id,
            t.description
        FROM Task t
        WHERE t.assignee_id = ?
        """
    tasks = db.execute(tasks_query, (user_id,)).fetchall()
    print('Tasks fetch successful')

    if projects is None:
        return None, "Not projects found for that user_id"
    projects_data = [dict(project) for project in projects]
    tasks_data = [dict(task) for task in tasks]

    return projects_data, tasks_data, None

def create_project(data):

    print("Hello")

    """
    Creates a new project in the database.
    :param data: Dictionary containing project_name, description, user_id, and status.
    :return: The newly created project's ID.
    """
    try:
        db = get_db()  # Get the current database connection
        cursor = db.execute(
            """
            INSERT INTO Project (project_name, description, user_id, status) 
            VALUES (?, ?, ?, ?)
            """,
            (data['project_name'], data['description'], data['user_id'], data.get('status', 'NOT STARTED'))
        )
        print("Successfully executed SQL query")
        print(data)

        
        
        db.commit()
        project_id = cursor.lastrowid 
         # Associate the project with the provided teams
        project_team_query = """
        INSERT INTO Project_Teams (project_id, team_id)
        VALUES (?, ?)
        """
        print("added project_teams")
        for team_id in data['team_ids']:
            db.execute(project_team_query, (project_id, team_id))
        db.commit()
        return cursor.lastrowid, None
    except Exception as e:
        # Raise the error to the controller to handle it
        return None , "Error creating project: " + str(e)
    
def update_project(project_id, data):
    """
    Updates an existing project in the database.
    :param project_id: The ID of the project to update.
    :param data: Dictionary containing project_name, description, user_id, and status.
    :return: Number of rows updated.
    """
    try:
        db = get_db()
        result = db.execute(
            """
            UPDATE Project
            SET project_name = ?, description = ?, status = ?
            WHERE project_id = ?
            """,
            (data['project_name'], data['description'], data['status'], project_id)
        )
        db.commit()
        return result.rowcount, None
    except Exception as e:
        return None, "Error updating project: " + str(e)
    
def delete_project(project_id):
    """
    Deletes a project from the database.
    :param project_id: The ID of the project to delete.
    :return: Number of rows deleted.
    """
    try:
        db = get_db()
        result = db.execute(
            "DELETE FROM Project WHERE project_id = ?", (project_id,)
        )
        db.commit()
        return result.rowcount, None
    except Exception as e:
        return None, "Error deleting project: "+ str(e)
    
def get_projects_by_team_id(team_id):
    """Get all projects associated with a specific team, including project name, status, and project id."""
    db = get_db()

    # Fetch all projects for the given team_id
    projects_query = """
    SELECT 
        p.project_id,
        p.project_name,
        p.status
    FROM Project p
    JOIN Project_Teams pt ON pt.project_id = p.project_id
    WHERE pt.team_id = ?
    """
    
    projects = db.execute(projects_query, (team_id,)).fetchall()
    print('projects query successful')

    if projects is None:
        return None, "Not projects found for that team_id"

    # Convert the result into a list of project details
    project_list = [
        {"project_id": project["project_id"], 
         "project_name": project["project_name"], 
         "status": project["status"]}
        for project in projects
    ]
    print(project_list)
    return project_list, None


def get_assignees_by_project_id(project_id):
    """Get all team members (assignees) for a specific project, including member name and role."""
    db = get_db()

    # Query to fetch all team members associated with the project, including their names and roles
    assignees_query = """
    SELECT 
        u.user_id,
        u.user_name AS member_name,
        tm.is_owner
    FROM Team_Members tm
    JOIN User u ON tm.user_id = u.user_id
    JOIN Project_Teams pt ON pt.team_id = tm.team_id
    WHERE pt.project_id = ?
    """
    print(assignees_query)
    assignees = db.execute(assignees_query, (project_id,)).fetchall()
    print('assignees query successful')

    if assignees is None:
        return None, "No team members found for the specified project."

    # Convert the result into a list of assignees (name and role)
    assignee_list = [
        {"user_id": assignee["user_id"],
         "member_name": assignee["member_name"],
         "is_owner": assignee["is_owner"]}
        for assignee in assignees
    ]
    print(assignee_list)
    return assignee_list, None
