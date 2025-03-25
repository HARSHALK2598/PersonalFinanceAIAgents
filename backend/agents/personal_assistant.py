from typing import Dict, Any
from .base_agent import BaseAgent
from .profile_agent import ProfileAgent
from .planner_agent import PlannerAgent
from rag.pipeline import RAGPipeline
from models.user_session import UserSession
from services.session_manager import SessionManager
import json

class PersonalAssistant(BaseAgent):
    def __init__(self):
        super().__init__("personal_assistant")
        self.profile_agent = ProfileAgent()
        self.planner_agent = PlannerAgent()
        self.rag_pipeline = RAGPipeline()
        self.session_manager = SessionManager()
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.log_info(f"Processing user input: {input_data.get('text', '')}")
            
            # Get or create session
            session_id = input_data.get("session_id")
            session = self.session_manager.get_session(session_id)
            if not session:
                session = self.session_manager.create_session()
            
            # Add user message to history
            session.add_message("user", input_data.get("text", ""))
            
            # Step 1: Analyze user profile (if not exists or needs update)
            if not session.user_profile:
                profile_result = await self.profile_agent.process(input_data)
                if not profile_result["success"]:
                    return profile_result
                session.update_profile(profile_result["data"])
            
            # Step 2: Get relevant context from RAG pipeline
            rag_result = await self.rag_pipeline.process_query(input_data.get("text", ""))
            if not rag_result["success"]:
                return rag_result
            
            # Step 3: Generate comprehensive financial plan
            planning_input = {
                "profile": session.user_profile,
                "goal": input_data.get("text", ""),
                "context": rag_result["data"],
                "conversation_history": [msg.dict() for msg in session.get_recent_messages(5)]
            }
            
            plan_result = await self.planner_agent.process(planning_input)
            if not plan_result["success"]:
                return plan_result
            
            # Add assistant response to history
            session.add_message("assistant", json.dumps(plan_result["data"]), plan_result["data"])
            
            # Update session
            self.session_manager.update_session(session)
            
            # Combine all results
            final_response = {
                "success": True,
                "message": "Comprehensive financial plan generated successfully",
                "data": {
                    "session_id": session.id,
                    "profile": session.user_profile,
                    "context": rag_result["data"],
                    "plan": plan_result["data"],
                    "conversation_history": [msg.dict() for msg in session.get_recent_messages(5)]
                }
            }
            
            return final_response
            
        except Exception as e:
            return await self.handle_error(e) 