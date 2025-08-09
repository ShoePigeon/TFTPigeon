from src.models.db import get_db
def create_task(data):
    """
    Creates a new task in the database.
    :param data: Dictionary containing task_name, description, deadline, priority, status, and project_id.
    :return: The newly created task's ID.
    """
    try:
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO Task (task_name, description, deadline, priority, status, project_id, assignee_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (data['task_name'], data['description'], data['deadline'], data['priority'], data['status'], data['project_id'], data['assignee_id'])
        )
        db.commit()
        return cursor.lastrowid, None
    except Exception as e:
        return None, "Error creating task: " + str(e)

def update_task(task_id, data):
    """
    Updates an existing task in the database.
    :param task_id: The ID of the task to update.
    :param data: Dictionary containing task_name, description, deadline, priority, status.
    :return: Number of rows updated.
    """
    try:
        db = get_db()
        print(data)
        result = db.execute(
            """
            UPDATE Task
            SET task_name = ?, description = ?, deadline = ?, priority = ?, status = ?
            WHERE task_id = ?
            """,
            (data['task_name'], data['description'], data['deadline'], data['priority'], data['status'], task_id)
        )
        db.commit()
        return result.rowcount, None
    except Exception as e:
       return None, "Error updating task: "+ str(e)
    

def delete_task(task_id):
    """
    Deletes a task from the database.
    :param task_id: The ID of the task to delete.
    :return: Number of rows deleted.
    """
    try:
        db = get_db()
        # Fetch the project_id associated with the task
        project_query = """
        SELECT project_id FROM Task WHERE task_id = ?
        """
        task = db.execute(project_query, (task_id,)).fetchone()

        if not task:
            return None, False, "Task not found."

        project_id = task["project_id"]

        # Delete the task
        delete_query = """
        DELETE FROM Task WHERE task_id = ?
        """
        db.execute(delete_query, (task_id,))
        db.commit()

        return project_id, True, None

    except Exception as e:
        return None, False, f"An error occurred: {str(e)}"