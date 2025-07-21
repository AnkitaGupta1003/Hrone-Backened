"""
Routers package for the FastAPI ecommerce application.

This package contains all API route handlers organized by functionality:
- products: Product management endpoints
- orders: Order management endpoints
"""

from fastapi import APIRouter
from .products_router import router as products_router
from .orders_router import router as orders_router

__all__ = ["products_router", "orders_router", "routers"]


def create_api_router() -> APIRouter:
    """
    Factory function to create a configured API router with common settings.
    This can be used if you want consistent configuration across all routers.
    """
    return APIRouter(
        responses={
            404: {"description": "Not found"},
            500: {"description": "Internal server error"}
        }
    )


routers = [
    (products_router, ["products"]),
    (orders_router, ["orders"]),
]