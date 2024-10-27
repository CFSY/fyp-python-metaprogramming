from functools import wraps
from typing import Any, Dict, Type
import inspect
import uuid


class TaskMetadata:
    def __init__(self, func):
        self.func = func
        self.id = str(uuid.uuid4())
        self.name = func.__name__
        self.signature = inspect.signature(func)
        self.doc = func.__doc__ or "No description available"

    @property
    def input_schema(self) -> Dict[str, Type]:
        return {
            name: param.annotation if param.annotation != inspect.Parameter.empty else Any
            for name, param in self.signature.parameters.items()
        }


class Task(type):
    """Task metaclass for creating task definitions"""
    _registry = {}

    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        if 'execute' in attrs:
            metadata = TaskMetadata(attrs['execute'])
            new_cls._metadata = metadata
            Task._registry[metadata.id] = new_cls
        return new_cls

    @classmethod
    def get_all_tasks(cls):
        return cls._registry


def task(func):
    """Decorator to create a task class from a function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Create a new task class dynamically
    task_name = f"{func.__name__.title()}Task"

    class DynamicTask(metaclass=Task):
        execute = staticmethod(func)
        __module__ = func.__module__

    DynamicTask.__name__ = task_name

    return DynamicTask