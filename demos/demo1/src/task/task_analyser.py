import ast
import inspect
from typing import Dict, Type, Any
from .decorators import Task


class TaskAnalyser:
    """Analyzes task definitions and extracts metadata"""

    @staticmethod
    def _remove_decorators(source: str) -> str:
        """Remove decorators from function source code"""
        # Parse the source code into an AST
        tree = ast.parse(source)

        # Find the function definition node
        func_def = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_def = node
                break

        if func_def is None:
            return source

        # Clear the decorator list
        func_def.decorator_list = []

        # Convert back to source code
        return ast.unparse(tree)

    @staticmethod
    def analyze_task(task_cls: Type) -> Dict[str, Any]:
        """Analyze a task class and return its metadata"""
        if not hasattr(task_cls, '_metadata'):
            raise ValueError(f"Invalid task class: {task_cls}")

        metadata = task_cls._metadata
        source = inspect.getsource(metadata.func)

        # Remove decorators from the source
        clean_source = TaskAnalyser._remove_decorators(source)

        return {
            'id': metadata.id,
            'name': metadata.name,
            'source': clean_source,
            'input_schema': metadata.input_schema,
            'doc': metadata.doc
        }

    @staticmethod
    def get_all_task_metadata() -> Dict[str, Dict[str, Any]]:
        """Get metadata for all registered tasks"""
        return {
            task_id: TaskAnalyser.analyze_task(task_cls)
            for task_id, task_cls in Task.get_all_tasks().items()
        }

