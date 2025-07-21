# routers/products.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
import re

from schemas_py import ProductCreate, ProductResponse, ProductsListResponse, CreateResponse

from database_py import get_products_collection
from utils_py import serialize_docs

router = APIRouter()

@router.post("/products", status_code=201, response_model=CreateResponse)
async def create_product(product: ProductCreate):
    """Create a new product"""
    try:
        products_collection = get_products_collection()
        product_dict = product.dict()
        result = products_collection.insert_one(product_dict)
        
        return JSONResponse(
            status_code=201,
            content={"id": str(result.inserted_id)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products", status_code=200, response_model=ProductsListResponse)
async def list_products(
    name: Optional[str] = Query(None, description="Filter by product name (supports partial search)"),
    size: Optional[str] = Query(None, description="Filter by size (e.g., large)"),
    limit: Optional[int] = Query(10, description="Number of products to return"),
    offset: Optional[int] = Query(0, description="Number of products to skip")
):
    """List products with optional filtering and pagination"""
    try:
        products_collection = get_products_collection()
        
        # Build query filter
        query_filter = {}
        
        if name:
            # Support partial/regex search for name
            query_filter["name"] = {"$regex": re.escape(name), "$options": "i"}
        
        if size:
            # Filter by size - assuming size is part of the product name
            # This creates an AND condition with name filter if both are present
            size_filter = {"$regex": f"\\b{re.escape(size)}\\b", "$options": "i"}
            if "name" in query_filter:
                # Combine filters using $and
                query_filter = {
                    "$and": [
                        {"name": query_filter["name"]},
                        {"name": size_filter}
                    ]
                }
            else:
                query_filter["name"] = size_filter
        
        # Get total count for the query
        total_count = products_collection.count_documents(query_filter)
        
        # Apply pagination and sorting
        cursor = products_collection.find(query_filter).sort("_id", 1).skip(offset).limit(limit)
        products = list(cursor)
        
        # Serialize products
        serialized_products = serialize_docs(products)
        
        return JSONResponse(
            status_code=200,
            content={
                "data": serialized_products,
                "total": total_count,
                "limit": limit,
                "offset": offset
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))