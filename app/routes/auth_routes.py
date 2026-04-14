from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from app.db import users
from app.models.user_model import UserCreate, UserLogin
from app.auth import create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


@router.post("/register")
def register(user: UserCreate):
    if users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User exists")

    users.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password)
    })

    return {"message": "User registered"}


@router.post("/login")
def login(user: UserLogin):
    db_user = users.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(str(db_user["_id"]))

    return {"token": token}