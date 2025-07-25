import uvicorn
from fastapi import FastAPI, BackgroundTasks
from bot.routers.agent_router import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from bot.services.reminder_service import scheduler
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Allow CORS for testing (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend url(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

# Run.
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
