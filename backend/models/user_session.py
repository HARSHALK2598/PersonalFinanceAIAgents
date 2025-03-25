from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

class ConversationMessage(BaseModel):
    id: str = str(uuid.uuid4())
    timestamp: datetime = datetime.now()
    role: str  # "user" or "assistant"
    content: str
    metadata: Optional[Dict[str, Any]] = None

class UserSession(BaseModel):
    id: str = str(uuid.uuid4())
    created_at: datetime = datetime.now()
    last_active: datetime = datetime.now()
    conversation_history: List[ConversationMessage] = []
    user_profile: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        message = ConversationMessage(role=role, content=content, metadata=metadata)
        self.conversation_history.append(message)
        self.last_active = datetime.now()
    
    def get_recent_messages(self, limit: int = 5) -> List[ConversationMessage]:
        return self.conversation_history[-limit:]
    
    def update_profile(self, profile_data: Dict[str, Any]):
        self.user_profile = profile_data
    
    def update_preferences(self, preferences: Dict[str, Any]):
        self.preferences = preferences 