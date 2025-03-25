from typing import Dict, Any
from .base_agent import BaseAgent
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

class ProfileAgent(BaseAgent):
    def __init__(self):
        super().__init__("profile_agent")
        self.llm = HuggingFaceHub(
            repo_id="google/flan-t5-small",
            model_kwargs={"temperature": 0.7, "max_length": 512}
        )
        
        self.profile_prompt = PromptTemplate(
            input_variables=["user_input"],
            template="""Analyze the following user input and extract key profile information:
            {user_input}
            
            Provide a structured analysis including:
            1. Financial goals
            2. Risk tolerance
            3. Time horizon
            4. Current financial situation
            5. Investment preferences
            
            Response:"""
        )
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.log_info(f"Processing profile analysis for input: {input_data}")
            
            # Generate profile analysis
            prompt = self.profile_prompt.format(user_input=input_data.get("text", ""))
            response = self.llm(prompt)
            
            # Parse the response into structured data
            sections = response.split("\n")
            profile = {
                "financial_goals": sections[0] if len(sections) > 0 else "",
                "risk_tolerance": sections[1] if len(sections) > 1 else "",
                "time_horizon": sections[2] if len(sections) > 2 else "",
                "current_situation": sections[3] if len(sections) > 3 else "",
                "investment_preferences": sections[4] if len(sections) > 4 else ""
            }
            
            return {
                "success": True,
                "message": "Profile analysis completed successfully",
                "data": profile
            }
            
        except Exception as e:
            return await self.handle_error(e)
