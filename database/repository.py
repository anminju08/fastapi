from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select,delete

from database.orm import ToDo

def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalars(select(ToDo)))

def get_todo_by_todo_id(session: Session, todo_id: int) -> ToDo | None:
    return session.scalar(select(ToDo).where(ToDo.id==todo_id))

def create_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit() #db에 저장됨
    session.refresh(instance=todo) #db에서 데이터 읽어옴 -> todo_id값이 반영됨
    return todo

def delete_todo(session: Session, id: int):
    session.query(ToDo).filter(ToDo.id==id).delete()
    session.commit()

def update_todo(session: Session, todo: ToDo, active:bool):
    session.query(ToDo).filter(ToDo.id==ToDo.id).update(
        {"is_done": active}
    )
    session.commit()