from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseExecutor(ABC):
    def __init__(self, worker_path: str):
        self.worker_path = worker_path

    @abstractmethod
    async def execute(self, inputs: Dict[str, Any]) -> Any:
        """Execute the task with given inputs"""
        pass

    @abstractmethod
    def cleanup(self):
        """Cleanup resources"""
        pass
