from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from datetime import date

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TransactionBase(BaseModel):
    title: str
    amount: float = Field(..., gt=0)         
    type: Literal["income", "expense"]
    category: str
    date: date

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    title: str | None = None
    amount: float | None = Field(None, gt=0)
    type: Literal["income", "expense"] | None = None
    category: str | None = None
    date: date | None = None

class TransactionOut(TransactionBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True