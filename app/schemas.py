#Validation data
from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ProductCreate(BaseModel):
    name: str
    price: int


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True


class CartCreate(BaseModel):
    product_id: int

class CartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    items: List[OrderItemResponse] = []

    class Config:
        orm_mode = True