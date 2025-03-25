from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from uagents import Context
from models.schemas import UserGoal
from agents.assistant_agent import assistant_agent, profile_agent, planner_agent
import asyncio

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            goal = UserGoal(text=data)
            ctx = Context()
            await ctx.request(assistant_agent.address, goal)
            await websocket.send_text("🧠 Your plan is being generated. Please wait...")
        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")
