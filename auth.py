from supabase_client import create_client
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
import os


url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)


router = APIRouter()


class AuthRequest(BaseModel):
    email: str
    password: str



def signup_user(auth: AuthRequest):
    result = supabase.auth.sign_up({
        "email": auth.email,
        "password": auth.password
    })
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"]["message"])
    return result

def login_user(auth: AuthRequest):
    result = supabase.auth.sign_in_with_password({
        "email": auth.email,
        "password": auth.password
    })
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"]["message"])
    return result



@router.post("/signup")
def signup(auth: AuthRequest):
    return signup_user(auth)

@router.post("/login")
def login(auth: AuthRequest):
    return login_user(auth)