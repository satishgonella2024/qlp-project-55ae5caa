from pydantic import BaseModel, validator

class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    @validator('title', 'description')
    def validate_input(cls, v):
        if len(v) > 100:
            raise ValueError('Input must be less than 100 characters')
        return v

class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str