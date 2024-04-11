from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class Todo(BaseModel):
    title: str
    description: str


class GetTodo(Todo):
    id: UUID = Field(default_factory=UUID, alias="_id")
    created_at: datetime
    updated_at: datetime
    completed: bool
