#main.py
from fastapi import HTTPException
from typing import List

from fastapi import FastAPI, Depends
from pydantic.main import BaseModel
from sqlalchemy.orm.session import Session

from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, delete_todo, update_todo
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema
from fastapi import Body

app = FastAPI()

@app.get("/")
def heath_check_handler():
    return {"ping":"pong"}
#
# @app.get("/todos", status_code=200)
# def get_todos_handler(
#         order: str | None = None,
#         session: Session = Depends(get_db),
# )-> ToDoListSchema:
#     todos: List[ToDo] = get_todos(session=session)
#     dtoTodos: List[ToDoSchema] = [ToDoSchema.from_orm(todo) for todo in todos]
#     if order and order == "DESC":
#         return ToDoListSchema.from_orm(dtoTodos[::-1])
#     return ToDoListSchema.from_orm(dtoTodos)

@app.get("/todosOrder")
def get_todos_handler(order: str | None = None, todo_data=None):
    ret = list(todo_data.values())
    if order and order == "DESC":
        return ret[::-1]
    return ret

#main.py
@app.get("/todos/{todo_id}",status_code=200)
def get_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db),
)-> ToDoSchema:
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


#main.py
@app.post("/todos", status_code=201)
def create_todo_hadler(
        request: CreateToDoRequest,
        session: Session = Depends(get_db),
) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request) # 이 시점에 id =none
    todo: ToDo = create_todo(session=session, todo=todo) # 이 시점에 id=int
    return ToDoSchema.from_orm(todo)

@app.delete("/todos/{id}")
def delete_todo_handler(id: int, session: Session = Depends(get_db)):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=id)
    todo: ToDo = delete_todo(session=session, id=id)
    return todo

class IsActive(BaseModel):
    is_done : bool
# @app.patch("/todos/{id}")
# def update_todo_handler(id: int, isActive: IsActive, session: Session = Depends(get_db)):
#     todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=id)
#     todo: ToDo | None = update_todo(session=session, todo=todo, active=isActive.is_done)
#     return todo


@app.get("/todos", status_code=200)
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db),
) -> ToDoListSchema:
    todos: List[ToDo] = get_todos(session=session)
    # ret = list(todo_data.values())
    if order and order == "DESC":
        return  ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
    )
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )

@app.patch("/todos/{todo_id}",status_code=200)
def update_todo_handler(
        todo_id:int,
        is_done:bool = Body(...,embed=True),
        session: Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        #update
        todo.done() if is_done else todo.undone()
        todo: ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")

@app.delete("/todos/{todo_id}", response_model=ToDoSchema)
def deleteToDo(
        todo_id: int,
        session: Session = Depends(get_db),
):
    todo : ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")

    delete_todo(session=session, todo=todo)
    return ToDoSchema.from_orm(todo)