# main.py
from fastapi import FastAPI
from routers import routers  # Now we can import directly from routers
from database_py import get_database, init_db

app = FastAPI()
# Initialize database connection
init_db()

# Include routers
for router, tags in routers:
    app.include_router(router, tags=tags)
@app.get("/")
async def root():
    return {"message": "Ecommerce API is running"}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Ecommerce API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from database_py import db
        # Test database connection
        db = get_database()
        db.command('ping')  # or 'hello'
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
