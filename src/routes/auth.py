import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from src.services.auth_service import register_user, authenticate_user, get_user_by_id, generate_validation_code, send_validation_email


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['dob']

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not dob:
            error = 'Date of Birth is required.'
        else:
            validation_code = generate_validation_code()
            error = register_user(username, email, password, dob, validation_code)

            if error is None:
                # Send email validation code
                send_validation_email(email, validation_code)
                flash("A validation code has been sent to your email. Please validate your email.")
                return redirect(url_for("auth.validate_email"))

        flash(error)

    return render_template('auth/register.html')

from src.services.auth_service import get_user_by_email, validate_user_email

@bp.route('/validate-email', methods=('GET', 'POST'))
def validate_email():
    if request.method == 'POST':
        email = request.form['email']
        code = request.form['code']

        # Get user by email
        user = get_user_by_email(email)

        if user is None:
            flash("Email not found.")
        elif user['email_validation_code'] != code:
            flash("Invalid validation code.")
        else:
            # Validate email through auth_service
            validate_user_email(email)
            flash("Email successfully validated. You can now log in.")
            return redirect(url_for("auth.login"))

    return render_template('auth/validate_email.html')

@bp.route('/test-login', methods=['POST'])
def test_login():
    data = request.json
    if 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400
    session['user_id'] = data['user_id']
    return jsonify({'message': 'Test login successful'})

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user, error = authenticate_user(username, password)

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = None if user_id is None else get_user_by_id(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html', user=g.user)
