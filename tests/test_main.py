from fastapi.testclient import TestClient

from database.orm import ToDo
from main import app

from fastapi.testclient import TestClient
from main import app

client = TestClient(app=app)

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}

def test_get_todos(client, mocker):
    #order =ASC
    mocker.patch("main.get_todos",return_value =[
        ToDo(id=1, contents="FastAPI Section 0",is_done=True),
        ToDo(id=2, contents="FastAPI Section 1", is_done=False),
    ])
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id":1, "contents": "FastAPI Section 0","is_done":True},
            {"id": 2, "contents": "FastAPI Section 1", "is_done": False},
        ]
    }

    #order =DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
    "todos": [
        {"id": 2, "contents": "FastAPI Section 1", "is_done": False},
        {"id": 1, "contents": "FastAPI Section 0", "is_done": True}
    ]
    }

    def test_create_todo(client, mocker):
        create_spy = mocker.spy(ToDo, "create")

        mocker.patch(
            "main.create_todo",
            return_value=ToDo(id=1, content="todo", is_done=True)
        )

        body = {
            "content": "test",
            "is_done": False,
        }
        response = client.post("/todos", json=body)

        assert create_spy.spy_return.id is None
        assert create_spy.spy_return.content == "test"
        assert create_spy.spy_return.is_done == False

        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "content": "todo",
            "is_done": True,
        }

#test_main.py


def test_update_todo(client,mocker):
    # 200
    undone = mocker.patch.object(ToDo,"undone")
    done = mocker.patch.object(ToDo, "done")

    mocker.patch(
        "main.get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="todo", is_done=True)
    )
    mocker.patch(
        "main.update_todo",
        return_value=ToDo(id=1, contents="todo", is_done=False)
    )

    response = client.patch("/todos/1", json={"is_done":True})

    done.assert_called_once()
    undone.assert_not_called()

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "contents": "todo",
        "is_done": False
    }

    # 404
    mocker.patch(
        "main.get_todo_by_todo_id",
        return_value=None
    )

    response = client.patch("/todos/1", json={"is_done": True})
    assert response.status_code == 404
    assert response.json() == {
        "detail": "ToDo Not Found"
    }
