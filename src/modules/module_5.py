from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import secrets

app = FastAPI()

# Pydantic model for Todo
class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    completed: bool = False

# In-memory todo list
todos: List[TodoItem] = []

# Get all todos
@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    return todos

# Create a new todo
@app.post("/todos", response_model=TodoItem, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoItem):
    todo.id = len(todos) + 1
    todos.append(todo)
    return todo

# Get a specific todo
@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int):
    try:
        return next(filter(lambda t: t.id == todo_id, todos))
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

# Update a todo
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    try:
        todo = next(filter(lambda t: t.id == todo_id, todos))
        todo.title = updated_todo.title
        todo.description = updated_todo.description
        todo.completed = updated_todo.completed
        return todo
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

# Delete a todo
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    try:
        todo = next(filter(lambda t: t.id == todo_id, todos))
        todos.remove(todo)
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )