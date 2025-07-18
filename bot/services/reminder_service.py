# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime, timedelta
# import uuid
# import asyncio
# from loguru import logger

# scheduler = BackgroundScheduler()
# scheduler.start()


# async def send_to_teams(user_id: str, message: str):
#     # Placeholder for actual Teams integration
#     logger.info(f"[{datetime.now()}] ⏰ Sending reminder to {user_id}: {message}")


# def reminder_job(user_id: str, message: str):
#     asyncio.run(send_to_teams(user_id, message))


# def schedule_reminder(user_id: str, message: str, minutes: int) -> dict:
#     job_id = str(uuid.uuid4())
#     run_time = datetime.now() + timedelta(minutes=minutes)

#     scheduler.add_job(
#         reminder_job,
#         'date',
#         run_date=run_time,
#         args=[user_id, message],
#         id=job_id,
#         replace_existing=True
#     )

#     logger.info(f"Reminder scheduled for {user_id} at {run_time} with message: {message}")

#     return {
#         "status": "scheduled",
#         "job_id": job_id,
#         "run_time": run_time.isoformat()
#     }



from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import uuid
import asyncio
from loguru import logger
from bot.services.teams import send_proactive_message

# Start background scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Async function to send to Teams
async def send_to_teams(user_id: str, message: str):
    try:
        logger.info(f"[{datetime.now()}] Sending reminder to {user_id}: {message}")
        await send_proactive_message(user_id, f"⏰ Reminder: {message}")
    except Exception as e:
        logger.exception(f"Failed to send reminder to {user_id}")

# Synchronous APScheduler-compatible wrapper
def reminder_job(user_id: str, message: str):
    asyncio.run(send_to_teams(user_id, message))

# Public function to schedule a reminder
def schedule_reminder(user_id: str, message: str, minutes: int) -> dict:
    job_id = str(uuid.uuid4())
    run_time = datetime.now() + timedelta(minutes=minutes)

    scheduler.add_job(
        reminder_job,
        'date',
        run_date=run_time,
        args=[user_id, message],
        id=job_id,
        replace_existing=True
    )

    logger.info(f"✅ Reminder scheduled for user '{user_id}' at {run_time} — Task: {message}")

    return {
        "status": "scheduled",
        "job_id": job_id,
        "run_time": run_time.isoformat()
    }
