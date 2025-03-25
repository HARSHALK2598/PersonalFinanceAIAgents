from pydantic import BaseModel
from typing import Optional, List

class UserGoal(BaseModel):
    text: str
    user_id: Optional[str] = None

class FinancialPlan(BaseModel):
    goal: str
    steps: List[str]
    timeline: str
    estimated_cost: Optional[str] = None
    risks: List[str] = []
    recommendations: List[str] = []

class AgentResponse(BaseModel):
    success: bool
    message: str
    data: Optional[FinancialPlan] = None
    error: Optional[str] = None
