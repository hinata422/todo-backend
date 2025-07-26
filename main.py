from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from auth import signup_user, login_user, AuthRequest
from auth import router as auth_router

app = FastAPI()

todos: List["ToDo"] = []

app.include_router(auth_router)

class ToDo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

@app.get("/")
def hello():
    return {"message": "Hello, backend!"}

@app.get("/todos")
def read_todos():
    return todos

@app.post("/todos")
def create_todo(todo: ToDo):
    todos.append(todo)
    return {"message": "タスクを追加しました", "todo": todo}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: ToDo):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[i] = updated_todo
            return {"message": "タスクを更新しました", "todo": updated_todo}
    raise HTTPException(status_code=404, detail="タスクが見つかりません")


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            deleted_todo = todos.pop(i)
            return {"message": "タスクを削除しました", "todo": deleted_todo}
    raise HTTPException(status_code=404, detail="タスクが見つかりません")

@app.post("/signup")
def signup(auth: AuthRequest):
    return signup_user(auth)

@app.post("/login")
def login(auth: AuthRequest):
    return login_user(auth)