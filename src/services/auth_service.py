from werkzeug.security import check_password_hash, generate_password_hash
from src.models.db import get_db
from src.services.notification_service import SENDER_EMAIL, SENDER_PASSWORD
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

def register_user(username, email, password, dob, validation_code):
    """Register a new user with a validation code."""
    db = get_db()
    try:
        db.execute(
            """
            INSERT INTO User (user_name, email, password, DOB, email_validation_code)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username, email, generate_password_hash(password), dob, validation_code),
        )
        db.commit()
    except db.IntegrityError as e:
        if "email" in str(e):
            return f"Email {email} is already registered."
        if "user_name" in str(e):
            return f"Username {username} is already registered."
        return "An error occurred during registration."
    return None


def authenticate_user(username, password):
    """Authenticate a user."""
    db = get_db()
    user = db.execute(
        'SELECT * FROM User WHERE user_name = ?', (username,)
    ).fetchone()

    if user is None:
        return None, 'Incorrect username.'
    if not check_password_hash(user['password'], password):
        return None, 'Incorrect password.'
    if not user['email_verified']:
        return None, 'Email not verified. Please validate your email.'
    return user, None


def get_user_by_id(user_id):
    """Retrieve user by ID."""
    db = get_db()
    return db.execute(
        'SELECT * FROM user WHERE user_id = ?', (user_id,)
    ).fetchone()

def send_validation_email(email, validation_code):
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD
    receiver_email = email

    subject = "Email Validation Code"
    body = f"Your email validation code is: {validation_code}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")  # Print the error

def generate_validation_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def get_user_by_email(email):
    """Retrieve user by email."""
    db = get_db()
    return db.execute(
        'SELECT * FROM User WHERE email = ?', (email,)
    ).fetchone()

def validate_user_email(email):
    """Mark the user's email as validated."""
    db = get_db()
    db.execute(
        'UPDATE User SET email_verified = 1, email_validation_code = NULL WHERE email = ?',
        (email,)
    )
    db.commit()

def get_all_users():
    """Retrieve all users with their username and email."""
    db = get_db()
    users = db.execute(
        'SELECT user_name AS username, email FROM User'
    ).fetchall()
    return [dict(user) for user in users]

