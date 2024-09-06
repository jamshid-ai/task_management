from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from jose.exceptions import JWTError
from ..core.elastic import get_elasticsearch_client  # Import Elasticsearch client setup
from pydantic import BaseModel
from ..config import settings



# Define a User model for Pydantic validation
class User(BaseModel):
    _id: str | None = None
    username: str
    role: str
    hashed_password: str

# Utility function to fetch the user from Elasticsearch
def get_user_from_elasticsearch(username: str) -> User:
    es = get_elasticsearch_client()  # Get Elasticsearch client

    # Query Elasticsearch to find the user by username
    query = {
        "query": {
            "match": {
                "username": username
            }
        }
    }

    # Search the user index for the username
    response = es.search(index="users", body=query)

    if not response['hits']['hits']:
        raise HTTPException(status_code=404, detail="User not found")

    # Extract the user document from the search results
    user_data = response['hits']['hits'][0]['_source']
    return User(**user_data)

# Function to extract the current user from the token and Elasticsearch
def get_current_user(token: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> User:
    # Decode and validate the token to extract the username
    try:
        payload = jwt.decode(token.credentials, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise JWTError
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user = get_user_from_elasticsearch(username)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return user
