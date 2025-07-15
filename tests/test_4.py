{
  "code": "import os
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# In-memory data store
todos = []

# Pydantic models
class Todo(BaseModel):
    id: int = None
    title: str
    description: str
    completed: bool = False
    created_at: datetime = None
    updated_at: datetime = None

class TodoCreate(BaseModel):
    title: str
    description: str

# Dependency for authentication
def authenticate(token: str = Depends('')):
    # Implement authentication logic here
    # e.g., validate token against a database or external service
    return True

# CRUD operations
@app.post('/todos', dependencies=[Depends(authenticate)])
def create_todo(todo: TodoCreate):
    new_todo = Todo(
        id=len(todos) + 1,
        title=todo.title,
        description=todo.description,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    todos.append(new_todo)
    return new_todo

@app.get('/todos', response_model=List[Todo], dependencies=[Depends(authenticate)])
def get_todos():
    return todos

@app.get('/todos/{todo_id}', response_model=Todo, dependencies=[Depends(authenticate)])
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail='Todo not found')

@app.put('/todos/{todo_id}', response_model=Todo, dependencies=[Depends(authenticate)])
def update_todo(todo_id: int, todo: TodoCreate):
    for i, existing_todo in enumerate(todos):
        if existing_todo.id == todo_id:
            updated_todo = Todo(
                id=todo_id,
                title=todo.title,
                description=todo.description,
                completed=existing_todo.completed,
                created_at=existing_todo.created_at,
                updated_at=datetime.now()
            )
            todos[i] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail='Todo not found')

@app.delete('/todos/{todo_id}', dependencies=[Depends(authenticate)])
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return {'message': 'Todo deleted'}
    raise HTTPException(status_code=404, detail='Todo not found')
",
  "tests": "import os
import pytest
from fastapi.testclient import TestClient
from main import app, Todo, TodoCreate

client = TestClient(app)

# Test data
todo_data = {
    'title': 'Test Todo',
    'description': 'This is a test todo'
}

def test_create_todo():
    response = client.post('/todos', json=todo_data)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == todo_data['title']
    assert data['description'] == todo_data['description']

def test_get_todos():
    response = client.get('/todos')
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_todo():
    response = client.get('/todos/1')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1

def test_update_todo():
    updated_data = {
        'title': 'Updated Todo',
        'description': 'This is an updated todo'
    }
    response = client.put('/todos/1', json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == updated_data['title']
    assert data['description'] == updated_data['description']

def test_delete_todo():
    response = client.delete('/todos/1')
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Todo deleted'
",
  "documentation": "This is a FastAPI application that provides a RESTful API for managing a todo list. It includes CRUD operations for creating, reading, updating, and deleting todos. The application uses Pydantic for data validation and includes a simple in-memory data store. Authentication is implemented as a dependency, but the actual authentication logic is not included in this example.",
  "dependencies": [
    "fastapi",
    "pydantic",
    "pytest"
  ]
}