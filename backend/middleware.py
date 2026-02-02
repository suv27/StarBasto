from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from database import get_product_price
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StarDefenseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.star_defense_key = "StarBasto_Secure_2026"

    async def dispatch(self, request: Request, call_next):
        # 1. Security Key Check
        auth_header = request.headers.get("X-Star-Defense-Key")
        if auth_header != self.star_defense_key:
            logger.warning("Invalid or missing X-Star-Defense-Key")
            return JSONResponse(status_code=403, content={"detail": "Security Alert: Invalid Key"})

        # 2. Price Validation Logic
        # We check any path containing "order" to ensure coverage
        if request.method == "POST" and "/order" in request.url.path:
            try:
                # Capture the body
                order_data = await request.json()
                items = order_data.get("items", [])
                
                for item in items:
                    barcode = item.get("barcode")
                    client_price_str = item.get("price")
                    
                    if not barcode or client_price_str is None:
                        continue

                    # Get the REAL price from your database.py
                    db_price = get_product_price(barcode)
                    
                    if db_price is not None:
                        client_price = float(client_price_str)
                        # Check for price tampering
                        if abs(client_price - db_price) > 0.001:
                            logger.error(f"TAMPERING DETECTED: {barcode} | Client: {client_price} | DB: {db_price}")
                            return JSONResponse(
                                status_code=403,
                                content={"detail": f"Security Alert: Price mismatch for item {barcode}"}
                            )
            except Exception as e:
                logger.error(f"Middleware Error: {e}")
                # If body parsing fails, we don't let it through
                return JSONResponse(status_code=400, content={"detail": "Invalid request body"})

        # If everything is fine, proceed to the actual route
        return await call_next(request)