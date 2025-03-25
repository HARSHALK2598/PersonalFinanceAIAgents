from typing import Dict, Any
from .base_agent import BaseAgent
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("planner_agent")
        self.llm = HuggingFaceHub(
            repo_id="google/flan-t5-small",
            model_kwargs={"temperature": 0.7, "max_length": 512}
        )
        
        self.planning_prompt = PromptTemplate(
            input_variables=["profile", "goal", "context"],
            template="""Based on the following information:
            
            User Profile:
            {profile}
            
            Financial Goal:
            {goal}
            
            Relevant Context:
            {context}
            
            Create a detailed financial plan including:
            1. Main goal
            2. Specific steps to achieve this goal
            3. Timeline
            4. Estimated costs
            5. Potential risks
            6. Recommendations
            
            Response:"""
        )
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.log_info(f"Processing financial plan for goal: {input_data.get('goal', '')}")
            
            # Generate financial plan
            prompt = self.planning_prompt.format(
                profile=input_data.get("profile", ""),
                goal=input_data.get("goal", ""),
                context=input_data.get("context", "")
            )
            response = self.llm(prompt)
            
            # Parse the response into structured data
            sections = response.split("\n")
            plan = {
                "goal": sections[0] if len(sections) > 0 else "",
                "steps": [s.strip() for s in sections[1].split(".") if s.strip()] if len(sections) > 1 else [],
                "timeline": sections[2] if len(sections) > 2 else "",
                "estimated_cost": sections[3] if len(sections) > 3 else "",
                "risks": [s.strip() for s in sections[4].split(".") if s.strip()] if len(sections) > 4 else [],
                "recommendations": [s.strip() for s in sections[5].split(".") if s.strip()] if len(sections) > 5 else []
            }
            
            return {
                "success": True,
                "message": "Financial plan generated successfully",
                "data": plan
            }
            
        except Exception as e:
            return await self.handle_error(e)
