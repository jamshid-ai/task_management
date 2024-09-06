from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    role: str
    hashed_password: str
