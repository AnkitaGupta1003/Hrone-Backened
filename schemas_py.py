# schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Product Schemas
class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Large T-Shirt",
                "price": 25.99,
                "quantity": 100
            }
        }

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    quantity: int
    
    class Config:
        schema_extra = {
            "example": {
                "id": "64a1b2c3d4e5f6789abcdef0",
                "name": "Large T-Shirt",
                "price": 25.99,
                "quantity": 100
            }
        }

class ProductsListResponse(BaseModel):
    data: List[ProductResponse]
    total: int
    limit: int
    offset: int

# Order Schemas
class OrderItem(BaseModel):
    productId: str
    boughtQuantity: int
    
    class Config:
        schema_extra = {
            "example": {
                "productId": "64a1b2c3d4e5f6789abcdef0",
                "boughtQuantity": 2
            }
        }

class OrderCreate(BaseModel):
    items: List[OrderItem]
    totalAmount: float
    userAddress: Dict[str, str]
    
    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {"productId": "64a1b2c3d4e5f6789abcdef0", "boughtQuantity": 2}
                ],
                "totalAmount": 51.98,
                "userAddress": {
                    "City": "New York",
                    "Country": "USA",
                    "ZipCode": "10001"
                }
            }
        }

class OrderResponse(BaseModel):
    id: str
    items: List[OrderItem]
    totalAmount: float
    userAddress: Dict[str, str]
    createdOn: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "id": "64a1b2c3d4e5f6789abcdef0",
                "items": [
                    {"productId": "64a1b2c3d4e5f6789abcdef0", "boughtQuantity": 2}
                ],
                "totalAmount": 51.98,
                "userAddress": {
                    "City": "New York",
                    "Country": "USA",
                    "ZipCode": "10001"
                },
                "createdOn": "2024-01-01T12:00:00"
            }
        }

class OrdersListResponse(BaseModel):
    data: List[OrderResponse]
    total: int
    limit: int
    offset: int

# Generic Response Schemas
class CreateResponse(BaseModel):
    id: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": "64a1b2c3d4e5f6789abcdef0"
            }
        }