import re
from bot.services.reminder_service import schedule_reminder


def reminder_agent(message: str) -> str:
    """
    Parse reminder time and task, schedule a reminder task.
    """
    try:
        time_match = re.search(r"(\d+)\s*(minutes?|mins?)", message.lower())
        if not time_match:
            return "Could not find a valid reminder time."

        minutes = int(time_match.group(1))
        reminder_text = re.sub(
            r"remind me in \d+\s*(minutes?|mins?) to", "", message, flags=re.IGNORECASE
        ).strip()

        # For now we use a placeholder user_id
        user_id = "user123"

        schedule_reminder(user_id, reminder_text, minutes)

        return f"⏰ Okay, I'll remind you to '{reminder_text}' in {minutes} minutes."
    except Exception as e:
        return "Failed to set reminder."
