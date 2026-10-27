#管HTTP
from app.repository import TodoRepository
from fastapi import FastAPI,Depends,Query
from app.exceptions import NotFoundError,DuplicateError
from fastapi.responses import JSONResponse
from app.schemas import TodoCreate
import json
from functools import lru_cache
from app.config import settings
from app.logging_conf import setup_logging
import logging
logger = logging.getLogger(__name__)

setup_logging(settings.log_level)

app = FastAPI()
logger.info("当前配置：%s",settings)


@lru_cache
def get_repo():
    return TodoRepository()

@app.exception_handler(NotFoundError)
def todo_id_notfound(request, exc):
    logger.warning("Todo %s not found", exc.todo_id)
    return JSONResponse(status_code=404, content={"detail": "Todo not found"})

@app.exception_handler(DuplicateError)
def duplicate_handler(request, exc):
    logger.warning("Title %s already exists",exc.title)
    return JSONResponse(status_code=409, content={"detail": "Title already exists"})

@app.post("/todos",status_code=201)
async def add_todo(todo:TodoCreate,repo: TodoRepository = Depends(get_repo)):
    res = repo.create(data=todo)
    logger.info("成功创建待办: id=%s", res.id)
    return res
    


@app.get("/todos/{todo_id}")
async def read_todo_id(todo_id:int,repo: TodoRepository = Depends(get_repo)):
    return repo.get(todo_id=todo_id)


@app.get("/todos")
async def read_todo(limit:int = Query(10,ge=1,le=100),repo: TodoRepository = Depends(get_repo)):
    return repo.list_all(limit=limit)

@app.put("/todos/{todo_id}")
async def update_todo_id(todo_id:int,data:TodoCreate,repo: TodoRepository = Depends(get_repo)):
    return repo.update(todo_id=todo_id,data=data)

@app.delete("/todos/{todo_id}",status_code=204)
async def delete_todo_id(todo_id:int,repo: TodoRepository = Depends(get_repo)):
    repo.delete(todo_id=todo_id)