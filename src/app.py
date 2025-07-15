import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from passlib.hash import bcrypt
from functools import lru_cache
from typing import List
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Environment variables for sensitive configuration
API_KEY = os.getenv('API_KEY')
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_MINUTES = 60

app = FastAPI()

origins = os.getenv('ALLOWED_ORIGINS').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.post("/token", response_model=UserOut)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in users if u['username'] == form_data.username), None)
    if not user or not bcrypt.verify(form_data.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = jwt.encode(
        {"sub": user["id"], "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    return {"id": user["id"], "username": user["username"], "access_token": access_token}

@app.post("/users", response_model=UserOut)
async def create_user(user: UserIn):
    existing_user = next((u for u in users if u['username'] == user.username), None)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_id = len(users) + 1
    password_hash = bcrypt.hash(user.password, rounds=12)
    new_user = {"id": user_id, "username": user.username, "password_hash": password_hash}
    users.append(new_user)
    return {"id": user_id, "username": user.username}

@app.get("/todos", response_model=List[TodoItem])
async def list_todos(current_user: dict = Depends(get_current_user)):
    return [todo for todo in todos if todo['user_id'] == current_user['id']]

@app.post("/todos", response_model=TodoItem)
async def create_todo(todo: TodoItem, current_user: dict = Depends(get_current_user)):
    todo_id = len(todos) + 1
    new_todo = {
        "id": todo_id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "user_id": current_user['id'],
    }
    todos.append(new_todo)
    return new_todo

@app.get("/todos/{todo_id}", response_model=TodoItem)
async def get_todo(todo_id: int, current_user: dict = Depends(get_current_user)):
    todo = next((t for t in todos if t['id'] == todo_id and t['user_id'] == current_user['id']), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, todo: TodoItem, current_user: dict = Depends(get_current_user)):
    existing_todo = next((t for t in todos if t['id'] == todo_id and t['user_id'] == current_user['id']), None)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    existing_todo.update({
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
    })
    return existing_todo

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, current_user: dict = Depends(get_current_user)):
    todo = next((t for t in todos if t['id'] == todo_id and t['user_id'] == current_user['id']), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.remove(todo)