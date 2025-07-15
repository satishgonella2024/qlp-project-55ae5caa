from fastapi import APIRouter
from ..models import TodoItem

todos_router = APIRouter()
todos = []

@todos_router.get("/todos")
def get_todos():
    return todos

@todos_router.post("/todos")
def create_todo(todo: TodoItem):
    todo.id = len(todos) + 1
    todos.append(todo.dict())
    return todo

@todos_router.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return {"error": "Todo not found"}

@todos_router.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoItem):
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            todos[i] = todo.dict()
            return todo
    return {"error": "Todo not found"}

@todos_router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            del todos[i]
            return {"message": "Todo deleted"}
    return {"error": "Todo not found"}