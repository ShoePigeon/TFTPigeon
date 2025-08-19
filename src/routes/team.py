from flask import Blueprint, flash, jsonify, redirect, render_template, request, session
from src.services.team_service import add_member_to_team, create_team, delete_member_from_team, delete_teaminfo, get_all_users, get_team, get_teams, update_teaminfo # Import the query_db function from your models
from src.services.project_service import  get_projects_by_team_id, get_assignees_by_project_id 
bp = Blueprint('team', __name__, url_prefix='/team')

@bp.route('/list',methods=['GET'])
def list_page():
    try:
        user_id = session.get('user_id') 
        teams,error =get_teams(user_id) 
        if error:
            return jsonify({'error': error}), 404
        users,error=get_all_users()
        return render_template('team/list.html', teams=teams,users=users, owner=user_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@bp.route('/create', methods=['POST'])
def create_teams():
    """
    Controller for creating a new project.
    :return: JSON response with the created project's ID and a success message.
    """
    try:
        team_name = request.form.get('team_name')
        description = request.form.get('description')
        owner_user_id = session.get('user_id')

        # Fetch multi-value field for assignees
        assignees = request.form.getlist('assignees')
          # Returns a list, e.g., ['2', '3', '4']
          

        # Validation
        if not team_name:
            return "Team name is required.", 400
        team= {"name":team_name,"description":description,"assignee":assignees}
        create_team(team)
        return redirect('/team/list')
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500
    

@bp.route('/update', methods=['POST'])
def update_team():
    """
    Controller for updating an existing team.
    :param team_id: ID of the team to update.
    :return: Redirect to the updated team's details or list page.
    """
    try:
        # Fetch the form data
        team_id= request.form.get('team_id')
        team_name = request.form.get('team_name')
        assignees = request.form.getlist('assignees')  # List of new assignees
        description = request.form.get('description')
        owner_id = request.form.get("owner_id")
        
        # Validation
        if not team_name:
            return "Team name is required.", 400
        team={}

        # Update the team details
        team["name"] = team_name
        team["assignee"] = assignees
        team['description'] = description
        team['owner_id'] =  owner_id
        team['team_id'] = team_id

        # Save changes to DB
        print(team)
        update_teaminfo(team)  # Replace with your update logic

        return redirect('/team/list')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@bp.route('/delete/<int:team_id>', methods=['POST'])
def delete_team(team_id):
    """
    Controller for deleting an existing team.
    :param team_id: ID of the team to delete.
    :return: Redirect to the team list page with a success or error message.
    """
    try:
        # Fetch the existing team (example query, replace with your ORM logic)
        team = get_team(team_id)  # Assume `get_team_by_id` fetches the team from DB

        if not team:
            return "Team not found.", 404

        # Delete the team
        delete_teaminfo(team_id)  # Replace with your delete logic

        return redirect('/team/list')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/get/<int:team_id>/', methods=['GET'])
def get_team_by_id(team_id=None):
    try:
        if not team_id:
            team_id = request.args.get('team_id', type=int)

        if not team_id:
            return jsonify({'error': 'Missing required field: project_id'}), 400

        # Fetch the project details by team_id
        projects, error = get_projects_by_team_id(team_id)
        print(projects)
        if  error:
            return jsonify({'error': error}), 404
        
        team,error= get_team(team_id)
        print(team)
        if  error:
            return jsonify({'error': error}), 404
        
        users,error =get_all_users()
        
        return render_template('team/info.html', projects=projects, team=team,users=users)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('add/member', methods=['POST'])
def add_member():
    """
    Adds a new member to a team with a specified role.

    :return: Redirects back to the team details page with an appropriate message.
    """
    try:
        # Extract data from the form
        team_id = request.form.get('team_id', type=int)
        user_id = request.form.get('member_name', type=int)
        is_owner = request.form.get('is_owner', type=int)  # 0 = Member, 1 = Owner

        if not team_id or not user_id:
            flash("Team ID and Member ID are required!", "error")
            return redirect(request.referrer)

        # Call the service function to add the member
        success, error = add_member_to_team(team_id, user_id, is_owner)

        if success:
            flash("Member added successfully!", "success")
        else:
            flash(error, "error")

        return redirect(f"/team/get/{team_id}")

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(request.referrer)

@bp.route('delete/member', methods=['POST'])
def delete_member():
    """
    Deletes a member from a team.

    :return: Redirects back to the team details page with an appropriate message.
    """
    try:
        # Extract data from the form
        team_id = request.form.get('team_id', type=int)
        user_id = request.form.get('member_id', type=int)

        if not team_id or not user_id:
            flash("Team ID and Member ID are required!", "error")
            return redirect(request.referrer)

        # Call the service function to delete the member
        success, error = delete_member_from_team(team_id, user_id)

        if success:
            flash("Member removed successfully!", "success")
        else:
            flash(error, "error")

        return redirect(f"/team/get/{team_id}")

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(request.referrer)