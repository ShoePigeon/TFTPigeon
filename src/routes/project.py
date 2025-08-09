from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify, session

from src.services.project_service import create_project, delete_project, update_project,get_project_by_id, get_projects_by_user_id
from src.services.team_service import get_teams

from datetime import datetime, timedelta

from collections import defaultdict

bp = Blueprint('project', __name__, url_prefix='/project')

@bp.route('/info')
def info_page():
    return render_template('project/info.html')


@bp.route('/list')
def list_page():
    """
    Fetch all projects and render them in the list.html template.
    """
    try:
        projects, tasks, error = get_projects_by_user_id(user_id=session.get("user_id"))  # Assuming user_id is provided
        teams = get_teams(session.get("user_id"))
        if error:
            return render_template('project/list.html', projects=[])
        return render_template('project/list.html', projects=projects, teams = teams[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @bp.route('/index')
# def index_page():
#     return render_template('dashboard/index.html')


# =======
# import functools
# from flask import Blueprint, flash, redirect, render_template, request, session, url_for
# from src.services.project_service import get_project_by_id

@bp.route('/create', methods=['GET', 'POST'])
def create_project_view():
    if request.method == 'POST':
        # Handle form submission
        pass
    teams = get_teams(session.get('user_id'))
    #print("this is the content",teams)
    return render_template('project/createProject.html',teams = teams[0] )

@bp.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        # Handle form submission
        pass
    return render_template('project/createTask.html')

@bp.route('/create_project', methods=['POST'])
def create_project_controller():

    """
    Controller for creating a new project.
    :return: JSON response with the created project's ID and a success message.
    """
    try:
        # Parse the JSON request body
        # data = request.get_json()

        # Check if the Content-Type is JSON
        if request.content_type == 'application/json':
            # Parse the JSON request body
            data = request.get_json()

        # Get logged-in user ID from session
        user_id = session.get('user_id')  # Ensure 'user_id' is set during login

        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        # Otherwise, parse the form data
        elif request.content_type == 'application/x-www-form-urlencoded' or request.content_type.startswith('multipart/form-data'):
            data = {
                'project_name': request.form.get('project_name'),
                'description': request.form.get('description'),
                'user_id': user_id,
                'status': request.form.get('status', 'Not Started'),
                'team_ids' : request.form.getlist('team_id')
            }
            
        else:
            return jsonify({'error': 'Unsupported Content-Type'}), 415



        # Validate required fields
        if not data['project_name'] or not data['description']:
            return jsonify({'error': 'Missing required fields'}), 400
        
        
        # Call the service layer
        project_id, error = create_project(data)

        #logging
        print("created project: "+str(project_id))

        if error is None:
            # return  jsonify({'project_id': project_id, 'message': 'Project created successfully!'}), 201
            # return render_template('/project/list.html')
            return redirect(url_for("project.list_page"))

        else:
            return jsonify({'error': error}), 400
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500
    
@bp.route('<int:team_id>/create_project', methods=['POST'])
def create_project_for_team(team_id):
    """
    Creates a project directly associated with a specific team.
    """
    try:
        
        # Extract form data
        project_name = request.form.get('project_name')
        description = request.form.get('description')
        status = request.form.get('status', 'NOT STARTED')
        user_id = session.get('user_id')  # Logged-in user ID

        if not project_name or not description:
            flash("Project name and description are required!", "error")
            return redirect(request.referrer)

        # Create the project associated with the team
        data={"project_name":project_name, "description":description, "user_id":user_id, "status":status, "team_ids":[team_id]}
        project_id, error = create_project(data)
        if error is None:
            flash("Project created successfully!", "success")
            return redirect(f'/team/get/{team_id}')
        else:
            flash(error, "error")
            return redirect(request.referrer)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(request.referrer)

@bp.route('/update_project', methods=['POST'])
def update_project_controller():
    try:
        # Extract form data
        project_id = request.form['project_id']
        project_name = request.form['project_name']
        description = request.form['description']
        status = request.form['status']

        # Create a data dictionary to pass to the update function
        data = {
            'project_name': project_name,
            'description': description,
            'status': status
        }

        # Validate the data if necessary
        if not project_id or not project_name or not description:
            flash("Missing required fields", "error")
            return redirect(request.referrer or '/default_url')

        # Call the update function
        rows_updated, error = update_project(project_id, data)

        if not error:
            flash("Project updated successfully!", "success")
        else:
            flash(f"Error: {error}", "error")

        # Redirect to the referring page or default page
        return redirect(request.referrer or '/default_url')

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(request.referrer or '/default_url')

    
@bp.route('/delete_project', methods=['POST'])
def delete_project_controller():
    """
    Controller for deleting a project.
    :return: JSON response with success or error message.
    """
    try:
        if request.content_type == 'application/json':
            # Handle JSON request
            data = request.get_json()
            project_id = data.get('project_id')
        else:
            # Handle form submission
            project_id = request.form.get('project_id')

        if not project_id:
            return jsonify({'error': 'Missing required field: project_id'}), 400

        # Call the delete_project service
        rows_deleted, error = delete_project(project_id)

        if error is None:
            flash("Project Deleted successfully!", "success")
            return redirect(request.referrer)
        else:
            flash(error, "error")
            return redirect(request.referrer)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(request.referrer)

 
def get_next_week_dates():
    today = datetime.now()  # Get today's date dynamically
    # Find the number of days to the next Sunday
    days_to_sunday = (7 - today.weekday()) % 7
    start_of_next_week = today + timedelta(days=days_to_sunday) - timedelta(days=2)  # Next Sunday
    end_of_next_week = start_of_next_week + timedelta(days=7)  # The following Saturday
    return start_of_next_week, end_of_next_week

# Function to convert string date to datetime object
def convert_to_datetime(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None  # Return None if conversion fails

 
@bp.route('/get/<int:project_id>', methods=['GET'])
def get_project_controller(project_id=None):
    try:
        if not project_id:
            project_id = request.args.get('project_id', type=int)

        if not project_id:
            return jsonify({'error': 'Missing required field: project_id'}), 400

        # Fetch project details (assuming the project has tasks)
        project, error = get_project_by_id(project_id)

        if not project or error:
            return jsonify({'error': error}), 404

        tasks = project.get('tasks', [])

        # Get next week's start and end date (Sunday start)
        start_of_next_week, end_of_next_week = get_next_week_dates()

        # Group tasks by day of the week
        tasks_due_next_week = defaultdict(list)
        # Week starts from Sunday
        days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        for task in tasks:
            deadline_str = task.get('deadline')  # Safely get the deadline
            if not deadline_str:  # Skip tasks without a deadline
                continue

            task_deadline = convert_to_datetime(deadline_str)  # Convert to datetime
            if not task_deadline:  # Skip tasks with invalid deadline format
                continue

            task_deadline += timedelta(days=1)  # Adjust deadline if valid

            if start_of_next_week <= task_deadline <= end_of_next_week:
                day_of_week = task_deadline.strftime('%A')
                tasks_due_next_week[day_of_week].append(task)
                
        # Pass grouped tasks to the template
        return render_template('project/info.html', project=project, tasks_due_next_week=tasks_due_next_week)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/get_by_user', methods=['GET'])
def get_projects_by_user_controller():
    """
    Controller for getting all projects associated with a user_id.
    :return: JSON response with the list of projects or an error message.
    """
    try:
        data = request.get_json()
        user_id = session.get('user_id') 

        if not user_id:
            return jsonify({'error': 'Missing required field: user_id'}), 400

        # Fetch all projects by user_id (replace with your actual data retrieval logic)
        projects, tasks , error = get_projects_by_user_id(user_id)

        if not projects or error:
            return jsonify({'error': error}), 404
        print(projects, "projects")
        return render_template("project/index.html", projects=projects)
        # return jsonify({'projects': projects}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
