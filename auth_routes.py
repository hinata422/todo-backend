from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from supabase_client import supabase
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()

app = FastAPI()

class AuthRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup_user(auth: AuthRequest):
    result = supabase.auth.sign_up({
        "email": auth.email,
        "password": auth.password
    })
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"]["message"])
    return result

@router.post("/login")
def login_user(auth: AuthRequest):
    result = supabase.auth.sign_in_with_password({
        "email": auth.email,
        "password": auth.password
    })
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"]["message"])
    return result