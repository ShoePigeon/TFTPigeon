import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src import create_app
from src.services.notification_service import send_all_deadlines, schedule_task_notifications

# Create the Flask application
app = create_app()

# Initialize AsyncIOScheduler
scheduler = AsyncIOScheduler()

# Add a job for send all deadlines in 7 days to the scheduler, this one runs every 10 seconds
# scheduler.add_job(func=send_all_deadlines, args=[app], trigger='cron', second='*/10')
# Run at 9:00 AM every day
scheduler.add_job(
    func=send_all_deadlines,
    args=[app],
    trigger='cron',
    hour=9,
    minute=0,
    second=0
)

# Periodically call schedule_task_notifications to check for new tasks
scheduler.add_job(
    func=schedule_task_notifications,
    args=[app, scheduler],
    trigger="interval",
    seconds=10  # Adjust this interval as needed
)

print("Scheduled job for dynamic task notifications.")

async def main():
    """
    Main async function to start the scheduler and run the Flask app using Hypercorn.
    """
    # # Start the scheduler
    # print("Starting the scheduler...")
    # scheduler.start()
    # print("Scheduler started.")
    # print("Scheduled jobs:", scheduler.get_jobs())

    # Configure and run Hypercorn to serve the Flask app
    config = Config()
    config.bind = ["127.0.0.1:5000"]  # Host and port
    await serve(app, config)

    # Shut down the scheduler gracefully when the app exits
    # scheduler.shutdown(wait=False)

if __name__ == "__main__":
    # Explicitly create a new event loop and run the main coroutine
    asyncio.run(main())

