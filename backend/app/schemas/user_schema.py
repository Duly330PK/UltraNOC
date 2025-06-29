from pydantic import BaseModel, Field
import uuid

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: str = "user"

class UserResponse(UserBase):
    id: uuid.UUID
    role: str

    class Config:
        from_attributes = True