from typing import Dict, Any, Tuple

from ..controller.code_generator import WorkerCodeGenerator
from ..executors.base import BaseExecutor
from ..executors.docker_executor import DockerExecutor
from ..executors.thread_executor import ThreadExecutor
from ..task.task_analyser import TaskAnalyser


class Controller:
    def __init__(self):
        self.task_analyzer = TaskAnalyser()
        self.code_generator = WorkerCodeGenerator()
        self.tasks = self.task_analyzer.get_all_task_metadata()
        self.active_executors: Dict[Tuple[str, str], BaseExecutor] = {}
        self.task_status: Dict[str, Dict] = {
            task_id: {"status": "idle", "result": None}
            for task_id in self.tasks.keys()
        }

    def get_executor(self, task_id: str, executor_type: str) -> BaseExecutor:
        """Get or create an executor for a task"""
        executor_key = (task_id, executor_type)

        if executor_key not in self.active_executors:
            worker_path = self.code_generator.generate_worker_code(
                self.tasks[task_id], executor_type
            )

            if executor_type == "thread":
                executor = ThreadExecutor(worker_path)
            elif executor_type == "docker":
                executor = DockerExecutor(worker_path)
            else:
                raise ValueError(f"Unknown executor type: {executor_type}")

            self.active_executors[executor_key] = executor

        return self.active_executors[executor_key]

    async def execute_task(self, task_id: str, executor_type: str, inputs: Dict[str, Any]) -> Any:
        """Execute a task with given inputs"""
        if task_id not in self.tasks:
            raise ValueError(f"Unknown task: {task_id}")

        self.task_status[task_id]["status"] = "running"
        self.task_status[task_id]["result"] = "..."

        try:
            executor = self.get_executor(task_id, executor_type)
            resp = await executor.execute(inputs)
            self.task_status[task_id]["status"] = resp["status"]
            self.task_status[task_id]["result"] = resp["result"]
            return resp
        except Exception as e:
            self.task_status[task_id]["status"] = "error"
            self.task_status[task_id]["result"] = str(e)
            raise

    def get_task_status(self, task_id: str) -> Dict:
        """Get the current status of a task"""
        return self.task_status.get(task_id, {"status": "unknown", "result": "unknown"})

    def cleanup(self):
        """Cleanup all resources"""
        for executor in self.active_executors.values():
            executor.cleanup()
        self.code_generator.cleanup_generated_code()
