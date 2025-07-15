import os
import pytest
from fastapi.testclient import TestClient
from main import app, Todo, TodoCreate

client = TestClient(app)

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