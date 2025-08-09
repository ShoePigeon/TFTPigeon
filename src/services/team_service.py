from flask import flash, session
from src.models.db import get_db


def get_teams(user_id):
    """
    Fetches teams data for a specific user by user_id, including team owners, description, and projects.

    :param user_id: The ID of the user whose teams need to be fetched.
    :return: A list of teams and an error message (if any).
    """
    try:
        db = get_db()
        print(user_id)

        # SQL query to fetch teams, members, owners, and projects
        teams = db.execute(
            """
            SELECT 
            t.team_id,
            t.team_name,
            t.description,
            GROUP_CONCAT(DISTINCT CASE WHEN tm.is_owner = 1 THEN tm_user.user_name END) AS team_owners,
           
            GROUP_CONCAT(DISTINCT tm_user.user_name) AS team_members,
            GROUP_CONCAT(DISTINCT p.project_id || ':' || p.project_name) AS projects
        FROM Team t
        JOIN Team_Members tm ON t.team_id = tm.team_id
        JOIN User tm_user ON tm.user_id = tm_user.user_id
        LEFT JOIN Project_Teams pt ON t.team_id = pt.team_id
        LEFT JOIN Project p ON pt.project_id = p.project_id
        WHERE t.team_id IN (
            SELECT team_id 
            FROM Team_Members 
            WHERE user_id = ?
        )
        GROUP BY t.team_id
        ORDER BY t.team_id;
            """,
            (user_id,)
        ).fetchall()
        # Check if any results were found
        if not teams:
            return [], None
        # Parse and format the results
        teams_data = []
        for team in teams:
            team_dict = dict(team)
            print("team dict: ",team_dict)

            # Parse the projects string into a list of dictionaries
            if team_dict.get("projects"):
                projects_list = []
                for project in team_dict["projects"].split(','):
                    project_id, project_name = project.split(':')
                    projects_list.append({
                        "project_id": int(project_id.strip()),
                        "project_name": project_name.strip(),
                    })
                team_dict["projects"] = projects_list
            else:
                team_dict["projects"] = []

            # Parse team members
            if team_dict.get("team_members"):
                team_dict["team_members"] = [
                    member.strip() for member in team_dict["team_members"].split(',')
                ]
            else:
                team_dict["team_members"] = []

            # Parse team owners
            if team_dict.get("team_owners"):
                team_dict["team_owners"] = [
                    owner.strip() for owner in team_dict["team_owners"].split(',')
                ]
            else:
                team_dict["team_owners"] = []

            # Append the formatted team dictionary
            teams_data.append(team_dict)

        return teams_data, None

    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def get_all_users():
    try:
        db = get_db()
        # Fetch all users for the dropdown
        users_query = "SELECT user_id, user_name FROM User"
        users = db.execute(users_query).fetchall()
        # Check if any results were found
        if not users:
            return None, "No users found"
        users_data=[dict(user) for user in users]
        return users_data,None
    except:
        return None, "Error Fetching Users"
    
def create_team(team):
    try:
        db = get_db()
        owner_id = session.get('user_id')
        # Insert the team
        team_query = """
        INSERT INTO Team (team_name, description)
        VALUES (?, ?)
        """

        cursor = db.execute(team_query, (team["name"], team['description']))
        team_id = cursor.lastrowid  # Get the ID of the newly inserted team

        # Insert team members (assignees)
        team_members_query = """
        INSERT INTO Team_Members (team_id, user_id, is_owner)
        VALUES (?, ?, ?)
        """
        # Add the owner as a member
        db.execute(team_members_query, (team_id, owner_id, 1))

        # Add each assignee as a member
        for assignee_id in team['assignee']:
            db.execute(team_members_query, (team_id, assignee_id, 0))

        db.commit()

        flash("Team added successfully!")
    except Exception as e:
        print(e)
        flash("Error adding team!")

def update_teaminfo(team):
    """
    Updates a team and its members in the database.
    """
    try:
        db = get_db()

        # Update the team name
        update_team_query = """
        UPDATE Team
        SET team_name = ?, description = ?
        WHERE team_id = ?
        """
        db.execute(update_team_query, (team['name'],team['description'], team['team_id']))

        # Delete all existing team members to re-insert updated ones
        delete_team_members_query = """
        DELETE FROM Team_Members
        WHERE team_id = ?
        """
        db.execute(delete_team_members_query, (team['team_id'],))

        # Re-insert updated team members (including the owner)
        insert_team_members_query = """
        INSERT INTO Team_Members (team_id, user_id, is_owner)
        VALUES (?, ?, ?)
        """
        # Add the owner
        db.execute(insert_team_members_query, (team['team_id'], team['owner_id'], True))

        # Add the updated assignees
        for assignee_id in team['assignee']:
            db.execute(insert_team_members_query, (team['team_id'], assignee_id, False))

        db.commit()

        flash("Team updated successfully!")
    except Exception as e:
        db.rollback()
        flash(f"Error updating team: {str(e)}")

def delete_teaminfo(team_id):
    """
    Deletes a team and its members from the database.
    """
    try:
        db = get_db()

        # Delete team members
        delete_team_members_query = """
        DELETE FROM Team_Members
        WHERE team_id = ?
        """
        db.execute(delete_team_members_query, (team_id,))

        # Delete the team itself
        delete_team_query = """
        DELETE FROM Team
        WHERE team_id = ?
        """
        db.execute(delete_team_query, (team_id,))

        db.commit()

        flash("Team deleted successfully!")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting team: {str(e)}")

def get_team(team_id):
    """
    Fetches a specific team's details by ID.

    :param team_id: The ID of the team to fetch.
    :return: A tuple containing the team details and an error message (if any).
    """
    try:
        db = get_db()

        # Query to fetch team details
        team_query = """
        SELECT t.team_id, t.team_name, t.description
        FROM Team t
        WHERE t.team_id = ?
        """
        team = db.execute(team_query, (team_id,)).fetchone()

        if not team:
            return None, "Team not found."

        # Query to fetch team owners
        owners_query = """
        SELECT u.user_name
        FROM Team_Members tm
        JOIN User u ON tm.user_id = u.user_id
        WHERE tm.team_id = ? AND tm.is_owner = 1
        """
        owners = db.execute(owners_query, (team_id,)).fetchall()

        # Query to fetch all team members (including owners)
        members_query = """
        SELECT u.user_name, tm.is_owner
        FROM Team_Members tm
        JOIN User u ON tm.user_id = u.user_id
        WHERE tm.team_id = ?
        """
        members = db.execute(members_query, (team_id,)).fetchall()

        # Format response
        team_details = {
            "team_id": team["team_id"],
            "team_name": team["team_name"],
            "description": team["description"],
            "team_owners": [owner["user_name"] for owner in owners],
            "team_members": [
                {
                    "user_name": member["user_name"],
                    "is_owner": member["is_owner"]
                }
                for member in members
            ]
        }

        return team_details, None

    except Exception as e:
        return None, f"An error occurred: {str(e)}"
    
def add_member_to_team(team_id, user_id, is_owner):
    """
    Adds a new member to a team in the database with a specified role.

    :param team_id: The ID of the team to which the member will be added.
    :param user_id: The ID of the user to be added as a member.
    :param is_owner: The role of the user (0 = Member, 1 = Owner).
    :return: A tuple (success, error_message).
    """
    try:
        db = get_db()

        # Check if the user is already a member of the team
        existing_member = db.execute(
            """
            SELECT 1
            FROM Team_Members
            WHERE team_id = ? AND user_id = ?
            """,
            (team_id, user_id)
        ).fetchone()

        if existing_member:
            return False, "User is already a member of the team."

        # Insert the new member into the Team_Members table
        db.execute(
            """
            INSERT INTO Team_Members (team_id, user_id, is_owner)
            VALUES (?, ?, ?)
            """,
            (team_id, user_id, is_owner)
        )
        db.commit()

        return True, None

    except Exception as e:
        return False, f"An error occurred: {str(e)}"
    

def delete_member_from_team(team_id, user_id):
    """
    Removes a member from a team.

    :param team_id: ID of the team.
    :param user_id: ID of the user to be removed.
    :return: Tuple (success: bool, error: str or None).
    """
    try:
        db = get_db()

        # Check if the member exists in the team
        member_query = """
        SELECT * FROM Team_Members
        WHERE team_id = ? AND user_id = ?
        """
        member = db.execute(member_query, (team_id, user_id)).fetchone()

        if not member:
            return False, "Member not found in the team."

        # Ensure the team still has at least one owner
        if member["is_owner"]:
            owner_count_query = """
            SELECT COUNT(*) AS owner_count
            FROM Team_Members
            WHERE team_id = ? AND is_owner = 1
            """
            owner_count = db.execute(owner_count_query, (team_id,)).fetchone()["owner_count"]

            if owner_count <= 1:
                return False, "Cannot remove the last owner of the team."

        # Delete the member from the team
        delete_query = """
        DELETE FROM Team_Members
        WHERE team_id = ? AND user_id = ?
        """
        db.execute(delete_query, (team_id, user_id))
        db.commit()

        return True, None

    except Exception as e:
        return False, f"An error occurred: {str(e)}"