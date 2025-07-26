from supabase import create_client, Client
from typing import Optional, List
from pydantic import BaseModel
from fastapi import HTTPException
import os


url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class ToDo(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False



def get_all_todos() -> List[dict]:
    response = supabase.table("todos").select("*").execute()
    if response.error:
        raise HTTPException(status_code=500, detail=response.error.message)
    return response.data

def create_todo(todo: ToDo) -> dict:
    response = supabase.table("todos").insert(todo.dict(exclude_unset=True)).execute()
    if response.error:
        raise HTTPException(status_code=500, detail=response.error.message)
    return response.data[0]

def update_todo(todo_id: int, updated_todo: ToDo) -> dict:
    response = supabase.table("todos").update(updated_todo.dict(exclude_unset=True)).eq("id", todo_id).execute()
    if response.error:
        raise HTTPException(status_code=500, detail=response.error.message)
    if not response.data:
        raise HTTPException(status_code=404, detail="指定されたIDのタスクが見つかりません")
    return response.data[0]

def delete_todo(todo_id: int) -> dict:
    response = supabase.table("todos").delete().eq("id", todo_id).execute()
    if response.error:
        raise HTTPException(status_code=500, detail=response.error.message)
    if not response.data:
        raise HTTPException(status_code=404, detail="指定されたIDのタスクが見つかりません")
    return response.data[0]