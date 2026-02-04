from fastapi import FastAPI, Request
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
import logging

# Import middleware and routers
from middleware import StarDefenseMiddleware
from database import get_product_price # Needed for middleware dependency
from routes import (
    inventory_router,
    catalog_router,
    cart_router,
    order_router
)

# Configure logging for main application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- FastAPI App Setup ---
app = FastAPI(
    title="StarBasto Backend API",
    description="API for managing inventory, catalog, cart, and orders with security middleware.",
    version="1.0.0"
)

# --- Middleware Configuration ---
# Provide the get_product_price function to the middleware.
# This is a simplified way to pass dependencies. In larger apps, use FastAPI's Dependency Injection more formally.
# The db_price_getter is a callable that the middleware will use.
middleware_list = [
    Middleware(StarDefenseMiddleware, db_price_getter=get_product_price)
]
app.add_middleware(*middleware_list)

# --- Include Routers ---
app.include_router(inventory_router)
app.include_router(catalog_router)
app.include_router(cart_router)
app.include_router(order_router)

# --- Root Endpoint ---
@app.get("/")
async def read_root():
    """Root endpoint to check if the API is online."""
    logger.info("GET / request received.")
    return {"status": "StarBasto API Online"}

# --- Health Check Endpoint ---
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("GET /health request received.")
    return {"status": "API is healthy"}

# --- To run this application ---
# 1. Ensure you are in the /Users/starmac07/GithubProjects/StarBasto/backend/ directory.
# 2. Install dependencies: pip install fastapi uvicorn python-multipart pytest redis
#    (Note: redis is not strictly used in this in-memory example but often included for future scalability)
# 3. Run the server: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
