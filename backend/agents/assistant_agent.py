from typing import Dict, Any
from rag.pipeline import RAGPipeline

class AssistantAgent:
    def __init__(self):
        self.rag_pipeline = RAGPipeline()
        
    async def process_goal(self, goal: str) -> Dict[str, Any]:
        return await self.rag_pipeline.process_query(goal)
