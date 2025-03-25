from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import UserGoal, AgentResponse
from agents.personal_assistant import PersonalAssistant
import json
import logging
from typing import List, Dict, Any
from models.user_session import UserSession
from services.session_manager import SessionManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Financial Coach API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the personal assistant
assistant = PersonalAssistant()
session_manager = SessionManager()

# Store active WebSocket connections
active_connections: Dict[str, WebSocket] = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = None
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                session_id = message.get("session_id")
                
                # Store connection
                if session_id:
                    active_connections[session_id] = websocket
                
                # Process message through Personal Assistant
                response = await assistant.process(message)
                
                # Send response back to client
                await websocket.send_json(response)
                
            except json.JSONDecodeError:
                await websocket.send_json({
                    "success": False,
                    "message": "Invalid JSON format",
                    "data": None
                })
                
    except WebSocketDisconnect:
        if session_id:
            active_connections.pop(session_id, None)
            logger.info(f"Client disconnected: {session_id}")
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {str(e)}")
        if session_id:
            active_connections.pop(session_id, None)
        await websocket.close()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Financial Coach API is running"}

# Knowledge Base Management Endpoints
@app.post("/api/advice")
async def add_advice(text: str, topic: str, category: str):
    """Add new financial advice to the knowledge base."""
    success = rag_pipeline.add_advice(text, topic, category)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to add advice")
    return {"message": "Advice added successfully"}

@app.get("/api/advice/category/{category}")
async def get_advice_by_category(category: str) -> List[Dict[str, Any]]:
    """Get financial advice by category."""
    advice = rag_pipeline.get_advice_by_category(category)
    return advice

@app.get("/api/advice/topic/{topic}")
async def get_advice_by_topic(topic: str) -> List[Dict[str, Any]]:
    """Get financial advice by topic."""
    advice = rag_pipeline.get_advice_by_topic(topic)
    return advice

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.dict()

@app.get("/sessions")
async def list_sessions():
    return {"sessions": [session.dict() for session in session_manager.get_active_sessions()]}

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    # Close WebSocket connection if active
    if session_id in active_connections:
        await active_connections[session_id].close()
        active_connections.pop(session_id)
    return {"message": "Session deleted successfully"}
