from flask import (
    Blueprint, render_template, jsonify, request, session
)

from src.services.project_service import create_project, delete_project, update_project,get_project_by_id, get_projects_by_user_id
from src.models.db import get_db
from src.services.team_service import get_teams

bp = Blueprint('blog', __name__)

@bp.route('/', methods=['GET'])
def index():
    """
    Controller for getting all projects associated with a user_id.
    :return: JSON response with the list of projects or an error message.
    """
    try:
        user_id = session.get('user_id') 

        if not user_id:
            return jsonify({'error': 'Missing required field: user_id'}), 400

        # Fetch all projects by user_id (replace with your actual data retrieval logic)
        projects,tasks, error = get_projects_by_user_id(user_id)

        if error:
            return jsonify({'error': error}), 404
        print(projects, "projects")
        teams = get_teams(user_id)
        print("print teams \n",teams)
        print("Tasks: ",tasks)
        return render_template("dashboard/index.html", projects=projects,teams=teams[0], tasks=tasks)
        # return jsonify({'projects': projects}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@bp.route('/calendar', methods=['GET'])
def calendar_view():
    try:
        project, error = get_project_by_id(1)

        all_tasks = []
        if project:
            tasks = project.get('tasks', [])
            if tasks:
                for task in tasks:
                    all_tasks.append({
                        'task_name': task['task_name'],
                        'deadline': task['deadline'],
                        'project_name': project['project_name']
                    })

        
        # Pass all_tasks to the template
        return render_template('calendar/index.html', tasks=all_tasks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
from datetime import datetime

@bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        db = get_db()
        user_id = session.get('user_id')
        project_query = """
        SELECT 
            p.project_id
        FROM Project p
        WHERE p.user_id = ?
        """

        projectIds = db.execute(project_query, (user_id, )).fetchall()

        total_tasks = []
        for row in projectIds:
            id = row['project_id']
            project, error = get_project_by_id(id)

            all_tasks = []
            tasks = project.get('tasks', [])
            for task in tasks:
                deadline = task['deadline']
                # Parse and format the deadline date (ignore time)
                deadline_date = datetime.strptime(deadline, '%Y-%m-%d').strftime('%Y-%m-%d')
                all_tasks.append({
                    'task_name': task['task_name'],
                    'deadline_date': deadline_date,  # Only the date, no time
                    'project_name': project['project_name']
                })
            total_tasks.extend(all_tasks)
        
        return jsonify(total_tasks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
