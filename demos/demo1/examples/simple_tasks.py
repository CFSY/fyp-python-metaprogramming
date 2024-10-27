from ..src.task.decorators import task
from ..src.web import app


@task
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@task
def multiply_numbers(x: float, y: float) -> float:
    """Multiply two numbers together"""
    return x * y

@task
def raise_exception():
    """Raise an exception"""
    raise

@task
def sleep_for_seconds(seconds: int) -> str:
    """Do nothing for 5 seconds"""
    sleep = __import__('time').sleep
    sleep(seconds)
    return "great nap!"

if __name__ == "__main__":
    app.run_server()
