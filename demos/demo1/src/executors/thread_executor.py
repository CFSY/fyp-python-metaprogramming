import asyncio
import importlib.util
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any

from .base import BaseExecutor


class ThreadExecutor(BaseExecutor):
    def __init__(self, worker_path: str):
        super().__init__(worker_path)
        self.thread_pool = ThreadPoolExecutor(max_workers=1)

        # Dynamically load the worker module
        spec = importlib.util.spec_from_file_location("worker", worker_path)
        self.worker_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.worker_module)

    async def execute(self, inputs: Dict[str, Any]) -> Any:
        loop = asyncio.get_event_loop()
        resp = await loop.run_in_executor(
            self.thread_pool,
            self.worker_module.execute_task,
            inputs
        )
        return resp

    def cleanup(self):
        self.thread_pool.shutdown()

    def __del__(self):
        """Destructor to ensure cleanup is called"""
        self.cleanup()
