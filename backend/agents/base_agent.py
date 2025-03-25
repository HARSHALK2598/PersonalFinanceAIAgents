from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the input data and return a response."""
        pass
    
    async def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle errors in a consistent way."""
        self.logger.error(f"Error in {self.name}: {str(error)}")
        return {
            "success": False,
            "message": f"Error in {self.name}",
            "error": str(error)
        }
    
    def log_info(self, message: str):
        """Log information messages."""
        self.logger.info(message)
    
    def log_error(self, message: str):
        """Log error messages."""
        self.logger.error(message) 