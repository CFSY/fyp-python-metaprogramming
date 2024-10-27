from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ..controller.controller import Controller


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    controller.cleanup()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
controller:Controller = None


class TaskExecutionRequest(BaseModel):
    executor_type: str
    inputs: Dict[str, Any]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page with all tasks"""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"tasks": controller.tasks}
    )


@app.get("/task/{task_id}", response_class=HTMLResponse)
async def task_page(request: Request, task_id: str):
    """Render the task detail page"""
    task = controller.tasks.get(task_id)
    if not task:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={
                "request": request,
            },
            status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="task.html",
        context={
            "task": task,
            "status": controller.get_task_status(task_id)
        }
    )


@app.post("/api/task/{task_id}/execute")
async def execute_task(task_id: str, execution_request: TaskExecutionRequest):
    """Execute a task with given inputs"""
    try:
        resp = await controller.execute_task(
            task_id,
            execution_request.executor_type,
            execution_request.inputs
        )
        return {"status": resp["status"], "result": resp["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/task/{task_id}/status")
async def get_task_status(task_id: str):
    """Get the current status of a task"""
    status = controller.get_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return status


def run_server():
    """Run the web server"""
    global controller
    controller = Controller()

    uvicorn.run(app, host="0.0.0.0", port=8000)
