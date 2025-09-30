from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session, select

from .models import Todo, TodoCreate, TodoRead, TodoUpdate


def create_todo(session: Session, data: TodoCreate) -> Todo:
    todo = Todo(title=data.title, description=data.description, done=data.done)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def list_todos(session: Session) -> List[Todo]:
    return session.exec(select(Todo).order_by(Todo.id)).all()


def get_todo_or_404(session: Session, todo_id: int) -> Todo:
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


def update_todo(session: Session, todo_id: int, patch: TodoUpdate) -> Todo:
    todo = get_todo_or_404(session, todo_id)
    if patch.title is not None:
        todo.title = patch.title
    if patch.description is not None:
        todo.description = patch.description
    if patch.done is not None:
        todo.done = patch.done
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def delete_todo(session: Session, todo_id: int) -> None:
    todo = get_todo_or_404(session, todo_id)
    session.delete(todo)
    session.commit()
