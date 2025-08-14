# src/routes/matchHistory.py
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify, session
from src.services.match_service import (
    # create_matchHistory,
    # delete_matchHistory,
    # update_matchHistory,
    # get_matchHistory_by_id,
    # get_matchHistory_by_user_id,
    get_match_info as get_match_info
)
from datetime import datetime

bp = Blueprint('match', __name__, url_prefix='/match')


# @bp.route('/list')
# def list_matches():
#     """
#     Fetch all matches for the logged-in user and render them.
#     """
#     try:
#         user_id = session.get("user_id")
#         if not user_id:
#             return jsonify({'error': 'User not logged in'}), 401

#         matches, error = get_matchHistory_by_user_id(user_id)
#         if error:
#             return render_template('match/list.html', matches=[])
#         return render_template('match/list.html', matches=matches)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @bp.route('/create', methods=['POST'])
# def create_match_controller():
#     """
#     Controller for creating a new match history record.
#     """
#     try:
#         user_id = session.get('user_id')
#         if not user_id:
#             return jsonify({'error': 'User not logged in'}), 401

#         if request.content_type == 'application/json':
#             data = request.get_json()
#         elif request.content_type.startswith('application/x-www-form-urlencoded') or request.content_type.startswith('multipart/form-data'):
#             data = {
#                 'user_id': user_id,
#                 'placement': request.form.get('placement'),
#                 'level': request.form.get('level'),
#                 'gold_left': request.form.get('gold_left'),
#                 'time_eliminated': request.form.get('time_eliminated'),
#                 'traits': request.form.get('traits'),   # expect JSON string or similar
#                 'units': request.form.get('units'),     # expect JSON string or similar
#                 'win': request.form.get('win') == 'true'
#             }
#         else:
#             return jsonify({'error': 'Unsupported Content-Type'}), 415

#         # Required fields check
#         if data.get('placement') is None or data.get('level') is None:
#             return jsonify({'error': 'Missing required match fields'}), 400

#         match_id, error = create_matchHistory(data)

#         if not error:
#             flash("Match history created successfully!", "success")
#             return redirect(url_for("matchHistory.list_matches"))
#         else:
#             flash(error, "error")
#             return redirect(request.referrer)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @bp.route('/update', methods=['POST'])
# def update_match_controller():
#     """
#     Controller for updating an existing match history record.
#     """
#     try:
#         match_id = request.form.get('match_id')
#         placement = request.form.get('placement')
#         level = request.form.get('level')
#         gold_left = request.form.get('gold_left')
#         win = request.form.get('win') == 'true'

#         if not match_id or not placement or not level:
#             flash("Missing required fields", "error")
#             return redirect(request.referrer)

#         data = {
#             'placement': placement,
#             'level': level,
#             'gold_left': gold_left,
#             'win': win
#         }

#         rows_updated, error = update_matchHistory(match_id, data)

#         if not error:
#             flash("Match history updated successfully!", "success")
#         else:
#             flash(error, "error")

#         return redirect(request.referrer)
#     except Exception as e:
#         flash(f"An error occurred: {str(e)}", "error")
#         return redirect(request.referrer)


# @bp.route('/delete', methods=['POST'])
# def delete_match_controller():
#     """
#     Controller for deleting a match history record.
#     """
#     try:
#         if request.content_type == 'application/json':
#             data = request.get_json()
#             match_id = data.get('match_id')
#         else:
#             match_id = request.form.get('match_id')

#         if not match_id:
#             return jsonify({'error': 'Missing required field: match_id'}), 400

#         rows_deleted, error = delete_matchHistory(match_id)

#         if not error:
#             flash("Match deleted successfully!", "success")
#         else:
#             flash(error, "error")

#         return redirect(request.referrer)
#     except Exception as e:
#         flash(f"An error occurred: {str(e)}", "error")
#         return redirect(request.referrer)


# @bp.route('/get/<int:match_id>', methods=['GET'])
# def get_match_controller(match_id=None):
#     """
#     Fetch a single match's details and render them.
#     """
#     try:
#         if not match_id:
#             match_id = request.args.get('match_id', type=int)

#         if not match_id:
#             return jsonify({'error': 'Missing match_id'}), 400

#         match, error = get_matchHistory_by_id(match_id)

#         if error:
#             return jsonify({'error': error}), 404

#         return render_template('match/info.html', match=match)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


@bp.route('/info', methods=['GET', 'POST'])
def match_info():
    if request.method == 'POST':
        username = request.form.get('username')
        game_tag = request.form.get('game_tag')

        if not username or not game_tag:
            flash('Please provide both username and game tag.', 'error')
            return redirect(url_for('match.match_info'))

        match, error = get_match_info(username, game_tag)

        if error:
            flash(f"Error fetching match info: {error}", 'error')
            return redirect(url_for('match.match_info'))

        # Pass match data to the template
        return render_template('match/info.html', match=match)

    # GET request - just show the empty form
    return render_template('match/info.html')