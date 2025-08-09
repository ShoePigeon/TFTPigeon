from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from src.services.task_service import create_task, delete_task, update_task 
from src.services.project_service import get_project_by_id

bp = Blueprint('task', __name__, url_prefix='/task')

@bp.route('/create', methods=['POST'])
def create_task_controller():
    """
    Controller for creating a task.
    """
    try:
        # Check the content type of the request
        if request.content_type == 'application/json':
            data = request.get_json()
        elif request.content_type == 'application/x-www-form-urlencoded' or request.content_type.startswith('multipart/form-data'):
            data = {
                'task_name': request.form.get('task_name'),
                'description': request.form.get('description'),
                'deadline': request.form.get('deadline'),
                'priority': request.form.get('priority'),
                'status': request.form.get('status'),
                'assignee_id': request.form.get('assignee_id'),
                'project_id': request.form.get('project_id'),  # Ensure project_id is passed
            }
        else:
            return jsonify({'error': 'Unsupported Content-Type'}), 415

       
        # Validate project_id
        project_id = data['project_id']
        if not project_id:
            return jsonify({'error': 'Invalid project ID'}), 400

        # Create task
        task_id, error = create_task(data)
        if error is None:
            # Redirect to the project information page
            flash("Task Added Successfully!")
            return redirect(f"/project/get/{project_id}")
        else:
            return jsonify({'error': error}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@bp.route('/update/', methods=['POST'])
def update_task_controller():
    """
    Controller for updating a task.
    :return: JSON response with success or error message.
    """
    taskboard =  False
    try:  
        project_id = request.form.get('project_id')
        if not project_id:
            taskboard = True
            # Get JSON data from the request
            data = request.get_json()
            task_id = data.get('task_id')
            project_id = data.get('project_id')
        else:
            task_id = request.form.get('task_id')
            data = {
                    'task_name': request.form.get('task_name'),
                    'description': request.form.get('description'),
                    'deadline': request.form.get('deadline'),
                    'priority': request.form.get('priority'),
                    'status': request.form.get('status'),
                    'assignee_id': request.form.get('assignee_id'),
                    'project_id': request.form.get('project_id'),  # Ensure project_id is passed
                }
        rows_updated = update_task(task_id, data)
        flash("Task Updated successfully!")
        if taskboard:
            return jsonify({
            'status': 'success',
            'message': 'Task Updated successfully!'
        }), 200
        return redirect(f'/project/get/{project_id}')
    except Exception as e:
        flash("Task could not be updated")
        return redirect(f'/project/get/{project_id}')

@bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task_controller(task_id):
    """
    Controller for deleting a task.
    :return: JSON response with success or error message.
    """
    try:
        projectid,success,error = delete_task(task_id)

        if error:
            return jsonify({'error': 'Task not found'}), 404
        flash("Task Deleted successfully!")
        return redirect(f'/project/get/{projectid}')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@bp.route('/project/<int:project_id>/taskboard', methods=['GET'])
def taskboard_view(project_id):
    # Fetch the project data using the helper function
    project_data, error = get_project_by_id(project_id)

    # If there's an error (e.g., project not found), handle it appropriately
    if error:
        return render_template('error.html', message=error), 404

    # Extract only the project name and tasks from the project_data
    project_name = project_data['project_name']
    tasks = project_data['tasks']

    print("tasks are-",tasks)

    # Pass only the project name and tasks to the template
    return render_template('task/TaskBoard.html', project_name=project_name, tasks=tasks, project_id = project_id)
