import os
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.models.db import get_db
from datetime import datetime, timedelta, time


# TODO: Move credentials to environment variables before production!
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "xurobert1205@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "gjkx fjtk fyjv dqko")

async def send_email(receiver_email, subject, body):
    """
    Send an email asynchronously with the specified subject and body.
    """
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        await aiosmtplib.send(
            msg,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=SENDER_EMAIL,
            password=SENDER_PASSWORD,
        )
        print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"Error sending email to {receiver_email}: {e}")


async def send_all_deadlines(app):
    """
    Notify users about their active tasks with upcoming deadlines.
    """
    print("send_all_deadlines: Executing job")
    with app.app_context():  # Use synchronous context manager for app context
        # Fetch tasks grouped by user
        tasks_by_user = get_active_tasks()

        for _, user_data in tasks_by_user.items():
            receiver_email = user_data["email"]
            user_name = user_data["user_name"]

            # Prepare email body
            task_list = "\n".join(
                [
                    f"- {task['task_name']} (Deadline: {task['deadline']}, Priority: {task['priority']})"
                    for task in user_data["tasks"]
                ]
            )
            body = (
                f"Hello {user_name},\n\n"
                "You have the following tasks with upcoming deadlines:\n\n"
                f"{task_list}\n\n"
                "Please make sure to complete them on time.\n\nBest regards,\nYour Team"
            )

            # Send email to the user (await the async function)
            await send_email(receiver_email, "Upcoming Task Deadlines", body)  # Await the async function
        
        print("send_all_deadlines: Completed job")

async def schedule_task_notifications(app, scheduler):
    """
    Dynamically schedule email notifications for tasks due in the future.
    """
    print("Scheduling task notifications...")
    with app.app_context():
        tasks = get_tasks_with_future_deadlines()

        for task in tasks:
            task_name = task["task_name"]
            deadline = task["deadline"]  # Now a datetime object
            user_name = task["user_name"]
            receiver_email = task["email"]

            # Calculate the notification time (24 hours before the deadline)
            notification_time = deadline - timedelta(hours=24)

            # Skip if the notification time is in the past
            if notification_time <= datetime.now():
                continue

            # Schedule the email notification
            job_id = f"notify_{task['task_id']}"
            scheduler.add_job(
                func=send_task_due_email,
                args=[receiver_email, user_name, task_name, deadline],
                trigger="date",
                run_date=notification_time,
                id=job_id,
                replace_existing=True
            )
            print(
                f"Scheduled email for user '{user_name}' (Email: {receiver_email}) "
                f"about task '{task_name}' due at {deadline}. "
                f"Notification will be sent at {notification_time}."
            )

        print("Task notifications scheduled.")


async def send_task_due_email(receiver_email, user_name, task_name, deadline):
    """
    Send an email notification for a task due in 24 hours.
    """
    print(f"Sending email for task '{task_name}' due at {deadline}.")
    subject = f"Reminder: Task '{task_name}' is due soon!"
    body = (
        f"Hello {user_name},\n\n"
        f"This is a reminder that your task '{task_name}' is due on {deadline}.\n\n"
        "Please make sure to complete it on time.\n\nBest regards,\nYour Team"
    )

    # Send the email
    await send_email(receiver_email, subject, body)

    print(f"Email sent for task '{task_name}'.")


async def send_due_soon_tasks(app):
    """
    Notify users about tasks due the next day.
    """
    print("send_due_soon_tasks: Executing job")
    with app.app_context():  
        tasks_by_user = get_tasks_due_soon()  # Function to fetch tasks due in 24hours

        for _, user_data in tasks_by_user.items():
            receiver_email = user_data["email"]
            user_name = user_data["user_name"]

            # Prepare email body
            task_list = "\n".join(
                [
                    f"- {task['task_name']} (Deadline: {task['deadline']}, Priority: {task['priority']})"
                    for task in user_data["tasks"]
                ]
            )
            body = (
                f"Hello {user_name},\n\n"
                "The following tasks are due tomorrow:\n\n"
                f"{task_list}\n\n"
                "Please ensure they are completed on time.\n\nBest regards,\nYour Team"
            )

            # Send email to the user
            from src.services.notification_service import send_email  # Adjust import if necessary
            await send_email(receiver_email, "Tasks Due Tomorrow", body)

        print("send_due_soon_tasks: Completed job")


def get_active_tasks():
    """
    Fetch tasks assigned to users with deadlines within the next 7 days.
    Returns a dictionary mapping user_id to their active tasks.
    """
    db = get_db()
    query = """
        SELECT 
            u.user_id,
            u.user_name,
            u.email,
            t.task_id,
            t.task_name,
            t.deadline,
            t.priority,
            t.status
        FROM 
            Task t
        JOIN 
            User u ON t.assignee_id = u.user_id
        WHERE 
            t.status != 'COMPLETED' AND 
            t.deadline BETWEEN datetime('now') AND datetime('now', '+7 days')
        ORDER BY 
            u.user_id, t.deadline;
    """
    tasks_by_user = {}
    rows = db.execute(query).fetchall()
    
    for row in rows:
        user_id = row["user_id"]
        if user_id not in tasks_by_user:
            tasks_by_user[user_id] = {
                "user_name": row["user_name"],
                "email": row["email"],
                "tasks": []
            }
        tasks_by_user[user_id]["tasks"].append({
            "task_id": row["task_id"],
            "task_name": row["task_name"],
            "deadline": row["deadline"],
            "priority": row["priority"],
            "status": row["status"]
        })
    return tasks_by_user


def get_tasks_with_future_deadlines():
    """
    Fetch tasks with deadlines in the future.
    """
    db = get_db()
    now = datetime.now()

    query = """
        SELECT
            t.task_id,
            t.task_name,
            t.deadline,
            u.user_name,
            u.email
        FROM Task t
        JOIN User u ON t.assignee_id = u.user_id
        WHERE t.deadline > ?
          AND t.status != 'COMPLETED'
    """
    rows = db.execute(query, (now,)).fetchall()

    tasks = []
    for row in rows:
        deadline_str = row["deadline"]
        try:
            # Try parsing as datetime with time
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                # Try parsing as date without time and default to 23:59:59
                deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                deadline = datetime.combine(deadline_date, time(23, 59, 59))
            except ValueError:
                raise ValueError(f"Invalid date format for deadline: {deadline_str}")

        tasks.append({
            "task_id": row["task_id"],
            "task_name": row["task_name"],
            "deadline": deadline,
            "user_name": row["user_name"],
            "email": row["email"]
        })

    return tasks


def get_tasks_due_soon():
    """
    Fetch tasks due in the next 24 hours grouped by user.
    """
    db = get_db()
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)

    query = """
        SELECT
            t.task_name,
            t.deadline,
            t.priority,
            u.user_id,
            u.user_name,
            u.email
        FROM Task t
        JOIN User u ON t.assignee_id = u.user_id
        WHERE t.deadline BETWEEN ? AND ?
          AND t.status != 'COMPLETED'
    """
    rows = db.execute(query, (tomorrow_start, tomorrow_end)).fetchall()

    tasks_by_user = {}
    for row in rows:
        user_id = row["user_id"]
        if user_id not in tasks_by_user:
            tasks_by_user[user_id] = {
                "user_name": row["user_name"],
                "email": row["email"],
                "tasks": []
            }
        tasks_by_user[user_id]["tasks"].append({
            "task_name": row["task_name"],
            "deadline": row["deadline"],
            "priority": row["priority"]
        })

    return tasks_by_user