
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Simulated Database Access --- 
# This function simulates fetching product price from the DB.
# In a full application, this would import get_product_price from your database module.
# For this self-contained middleware example, we'll use a mock.

def get_simulated_db_price(barcode: str) -> float | None:
    mock_db = {
        "RICE001": 2.50,
        "SALAMI002": 5.00,
        "PRESIDENTE003": 3.75,
    }
    return mock_db.get(barcode)

# --- Middleware --- 

class StarDefenseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.star_defense_key = "StarBasto_Secure_2026" # Hardcoded temporary key

    async def dispatch(self, request: Request, call_next):
        # 1. Security Key Check
        auth_header = request.headers.get("X-Star-Defense-Key")
        if auth_header != self.star_defense_key:
            return JSONResponse(status_code=403, content={"detail": "Invalid Key"})

        # 2. Updated Path Logic
        if request.method == "POST" and "/order" in request.url.path:
            order_data = await request.json()
            items = order_data.get("items", [])
            
            for item in items:
                db_price = get_simulated_db_price(item.get("barcode"))
                if db_price is not None:
                    request_price = float(item.get("price", 0))
                    # Strict comparison
                    if abs(request_price - db_price) > 0.001:
                         return JSONResponse(
                             status_code=403, 
                             content={"detail": f"Security Alert: Price mismatch for {item.get('barcode')}"}
                         )

        return await call_next(request)