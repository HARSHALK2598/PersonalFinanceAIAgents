from typing import Dict, Any, Optional
from models.user_session import UserSession
import json
import os
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self, storage_dir: str = "./data/sessions"):
        self.storage_dir = storage_dir
        self.active_sessions: Dict[str, UserSession] = {}
        self._ensure_storage_dir()
        self._load_sessions()
    
    def _ensure_storage_dir(self):
        """Ensure the storage directory exists."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
    
    def _load_sessions(self):
        """Load all sessions from storage."""
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                session_id = filename[:-5]  # Remove .json extension
                self._load_session(session_id)
    
    def _load_session(self, session_id: str):
        """Load a specific session from storage."""
        filepath = os.path.join(self.storage_dir, f"{session_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                session = UserSession(**data)
                self.active_sessions[session_id] = session
    
    def _save_session(self, session: UserSession):
        """Save a session to storage."""
        filepath = os.path.join(self.storage_dir, f"{session.id}.json")
        with open(filepath, 'w') as f:
            json.dump(session.dict(), f, default=str)
    
    def create_session(self) -> UserSession:
        """Create a new user session."""
        session = UserSession()
        self.active_sessions[session.id] = session
        self._save_session(session)
        return session
    
    def get_session(self, session_id: str) -> Optional[UserSession]:
        """Get a session by ID."""
        return self.active_sessions.get(session_id)
    
    def update_session(self, session: UserSession):
        """Update a session and save it."""
        self.active_sessions[session.id] = session
        self._save_session(session)
    
    def cleanup_inactive_sessions(self, days: int = 30):
        """Remove sessions inactive for more than specified days."""
        cutoff = datetime.now() - timedelta(days=days)
        for session_id, session in list(self.active_sessions.items()):
            if session.last_active < cutoff:
                del self.active_sessions[session_id]
                filepath = os.path.join(self.storage_dir, f"{session_id}.json")
                if os.path.exists(filepath):
                    os.remove(filepath)
    
    def get_active_sessions(self) -> Dict[str, UserSession]:
        """Get all active sessions."""
        return self.active_sessions 