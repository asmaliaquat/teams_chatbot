# bot/services/teams.py

import os
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext,
    ConversationState,
    MemoryStorage
)
from botbuilder.schema import Activity, ActivityTypes

APP_ID = os.getenv("MICROSOFT_APP_ID")
APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD")

adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

memory = MemoryStorage()
conversation_state = ConversationState(memory)

# Store references to send messages later
conversation_references = {}

async def on_message_activity(turn_context: TurnContext):
    reference = TurnContext.get_conversation_reference(turn_context.activity)
    user_id = turn_context.activity.from_property.id
    conversation_references[user_id] = reference

    await turn_context.send_activity("Got it! I’ll remind you later.")

async def handle_bot_activity(activity: Activity, auth_header: str):
    async def logic(context: TurnContext):
        if context.activity.type == ActivityTypes.message:
            await on_message_activity(context)

    await adapter.process_activity(activity, auth_header, logic)

async def send_proactive_message(user_id: str, message: str):
    reference = conversation_references.get(user_id)
    if not reference:
        print(f"No conversation reference found for user {user_id}")
        return

    async def logic(turn_context: TurnContext):
        await turn_context.send_activity(message)

    await adapter.continue_conversation(reference, logic, APP_ID)
