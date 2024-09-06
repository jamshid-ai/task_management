from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from .dependencies import get_user_from_elasticsearch
from ..core.elastic import get_elasticsearch_client

# Replace these with your environment variables or config settings
from ..config import settings

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI Router for auth-related routes
router = APIRouter()

# Pydantic models for request and response validation
class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # Can be 'user' or 'admin'

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

# Endpoint to register a new user
@router.post("/register", response_model=Token)
async def register_user(user: UserCreate):
    es = get_elasticsearch_client()

    # Check if user already exists
    try:
        existing_user = get_user_from_elasticsearch(user.username)
        raise HTTPException(status_code=400, detail="Username already registered")
    except HTTPException as e:
        if e.status_code != 404:
            raise e

    # Hash the user's password
    hashed_password = get_password_hash(user.password)

    # Create user document
    user_doc = {
        "username": user.username,
        "hashed_password": hashed_password,
        "role": user.role
    }

    # Save the user to Elasticsearch
    es.index(index="users", body=user_doc)

    # Generate access token for the new user
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint to login and get a JWT token
@router.post("/token", response_model=Token)
async def login_for_access_token(username: str, password: str):
    try:
        user = get_user_from_elasticsearch(username)
    except HTTPException:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Generate access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Function to decode and verify JWT token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise JWTError
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    return token_data
