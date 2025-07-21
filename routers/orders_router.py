# routers/orders.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from bson import ObjectId
from datetime import datetime

from schemas_py import OrderCreate, OrderResponse, OrdersListResponse, CreateResponse
from database_py import get_orders_collection, get_products_collection
from utils_py import serialize_docs, validate_object_id

router = APIRouter()

@router.post("/orders", status_code=201, response_model=CreateResponse)
async def create_order(order: OrderCreate):
    """Create a new order"""
    try:
        products_collection = get_products_collection()
        orders_collection = get_orders_collection()
        
        # Validate that all products exist and have sufficient quantity
        for item in order.items:
            if not validate_object_id(item.productId):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid product ID: {item.productId}"
                )
            
            product = products_collection.find_one({"_id": ObjectId(item.productId)})
            if not product:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Product not found: {item.productId}"
                )
            
            if product["quantity"] < item.boughtQuantity:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient quantity for product {item.productId}. "
                           f"Available: {product['quantity']}, Requested: {item.boughtQuantity}"
                )
        
        # Update product quantities
        for item in order.items:
            products_collection.update_one(
                {"_id": ObjectId(item.productId)},
                {"$inc": {"quantity": -item.boughtQuantity}}
            )
        
        # Create order
        order_dict = order.dict()
        order_dict["createdOn"] = datetime.utcnow()
        # For demonstration purposes, we'll extract user_id from userAddress
        # In a real application, this would come from authentication
        order_dict["user_id"] = order_dict["userAddress"].get("City", "default_user")
        
        result = orders_collection.insert_one(order_dict)
        
        return JSONResponse(
            status_code=201,
            content={"id": str(result.inserted_id)}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/{user_id}", status_code=200, response_model=OrdersListResponse)
async def get_user_orders(
    user_id: str,
    limit: Optional[int] = Query(10, description="Number of orders to return"),
    offset: Optional[int] = Query(0, description="Number of orders to skip")
):
    """Get list of orders for a specific user"""
    try:
        orders_collection = get_orders_collection()
        
        # Filter by user_id
        query_filter = {"user_id": user_id}
        
        # Get total count for the query
        total_count = orders_collection.count_documents(query_filter)
        
        # Apply pagination and sorting
        cursor = orders_collection.find(query_filter).sort("_id", 1).skip(offset).limit(limit)
        orders = list(cursor)
        
        # Serialize orders
        serialized_orders = serialize_docs(orders)
        
        return JSONResponse(
            status_code=200,
            content={
                "data": serialized_orders,
                "total": total_count,
                "limit": limit,
                "offset": offset
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))