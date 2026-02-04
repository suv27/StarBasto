
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Simulated Database Access --- 
# This function simulates fetching product price from the DB.
# In a full application, this would import get_product_price from your database module.
# For this self-contained middleware example, we'll use a mock or ensure it's accessible.

# Mock function for demonstration if direct import is problematic in this context
def get_simulated_db_price(barcode: str) -> float | None:
    # This should ideally mirror or import from the actual database module
    mock_db = {
        "RICE001": 2.50,
        "SALAMI002": 5.00,
        "PRESIDENTE003": 3.75,
    }
    return mock_db.get(barcode)

# --- Middleware --- 

class StarDefenseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, db_price_getter):
        super().__init__(app)
        self.star_defense_key = "StarBasto_Secure_2026" # Hardcoded temporary key
        self.db_price_getter = db_price_getter # Dependency injection for DB access

    async def dispatch(self, request: Request, call_next):
        # Log incoming request method and path
        # logging.info(f"Incoming request: {request.method} {request.url.path}") # Logging might be too verbose for every request

        # 1. Security Key Check
        auth_header = request.headers.get("X-Star-Defense-Key")
        if not auth_header or auth_header != self.star_defense_key:
            logger.warning("Missing or invalid X-Star-Defense-Key")
            raise HTTPException(status_code=403, detail="Security Alert: Invalid or missing X-Star-Defense-Key")

        # 2. Price Validation for POST /orders (or checkout endpoint)
        # Ensure this check applies to the endpoint that *finalizes* the order,
        # which is typically the one that confirms purchase after cart items are finalized.
        # Let's assume it's /client/order for now.
        if request.method == "POST" and request.url.path == "/client/order":
            try:
                order_data = await request.json()
                items = order_data.get("items", [])
                
                if not items:
                    logger.warning("Order data is empty.")
                    # Allow empty orders to proceed, subsequent logic can handle it.
                    return await call_next(request)

                for item in items:
                    barcode = item.get("barcode")
                    # The price sent by the client in the order request
                    request_price_str = item.get("price") 

                    if not barcode or request_price_str is None:
                        logger.warning(f"Skipping price validation for item due to missing barcode or price: {item}")
                        continue # Skip validation if essential data is missing for this item

                    try:
                        request_price = float(request_price_str)
                    except ValueError:
                        logger.error(f"Invalid price format received for barcode {barcode}: {request_price_str}")
                        raise HTTPException(status_code=400, detail=f"Security Alert: Invalid price format for item {barcode}")

                    # Retrieve price from our simulated DB using the injected getter
                    db_price = self.db_price_getter(barcode)

                    if db_price is None:
                        logger.warning(f"Product barcode {barcode} not found in DB. Skipping price validation for this item.")
                        continue # Cannot validate if product is not found

                    # Strict price comparison: must match exactly within RD$0.01 tolerance
                    # Requirement: "if they don't match, block the order"
                    # Using a small tolerance for float comparison. If prices are clean strings like "2.50",
                    # direct float conversion and comparison is usually fine.
                    if abs(request_price - db_price) > 0.0001: # Check for exact match with float tolerance
                         logger.warning(f"Price mismatch for barcode {barcode}: Request price {request_price}, DB price {db_price}")
                         raise HTTPException(status_code=403, detail=f"Security Alert: Price mismatch for item {barcode}. Your price does not match the source of truth.")

            except Exception as e:
                logger.error(f"Error during order price validation: {e}")
                if isinstance(e, HTTPException):
                    raise e
                else:
                    raise HTTPException(status_code=500, detail="Internal Server Error during order processing.")

        # Proceed to the next middleware or route handler
        response = await call_next(request)
        # logging.info(f"Response: {response.status_code} {request.url.path}")
        return response
