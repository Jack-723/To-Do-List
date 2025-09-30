from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    done: bool = False


class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class TodoCreate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: int
    created_at: datetime


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None
