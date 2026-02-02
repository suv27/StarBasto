
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from database import search_products, update_order_status, register_owner

# Import database functions
from database import (
    get_all_products,
    update_product_details,
    get_product_price
)

# --- Pydantic Models ---

class ProductUpdateItem(BaseModel):
    barcode: str
    name: str
    price: str # Keep as string as per database schema
    stock_count: int

class OrderItem(BaseModel):
    barcode: str
    quantity: int
    price: str # Client sends their perceived price, middleware validates against DB

class OrderRequest(BaseModel):
    items: List[OrderItem]

class OrderResponse(BaseModel):
    message: str
    subtotal: float
    service_fee: float
    total_to_pay: float

class OwnerAccount(BaseModel):
    owner_id: str
    shop_name: str
    location: str

class OwnerRegistration(BaseModel):
    owner_id: str
    shop_name: str
    location: str
# --- Routers ---

# Owner Router
owner_router = APIRouter(prefix="/owner", tags=["Owner"])

@owner_router.post("/update-item")
async def update_item(item: ProductUpdateItem):
    """
    Owner API: Update or add a product item.
    Overwrites existing item if barcode matches.
    """
    success = update_product_details(
        barcode=item.barcode,
        name=item.name,
        price=item.price,
        stock_count=item.stock_count
    )
    if success:
        return {"message": f"Product with barcode {item.barcode} updated successfully."}
    else:
        raise HTTPException(status_code=500, detail="Failed to update product.")


@owner_router.post("/register")
async def setup_account(account: OwnerAccount):
    register_owner(account.owner_id, account.shop_name, account.location)
    return {"message": f"Welcome {account.shop_name}! Your StarBasto account is active."}

@owner_router.post("/register")
async def setup_account(data: OwnerRegistration):
    profile = register_owner(data.owner_id, data.shop_name, data.location)
    return {"message": "Account created successfully!", "profile": profile}

# Client Router
client_router = APIRouter(prefix="/client", tags=["Client"])

@client_router.get("/search")
async def find_product(q: str):
    results = search_products(q)
    return {"results": results}

@owner_router.patch("/order/{order_id}/status")
async def change_status(order_id: str, status: str):
    success = update_order_status(order_id, status)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": f"Order {order_id} updated to {status}"}

@client_router.get("/items")
async def get_items():
    """
    Client API: Get all available products.
    """
    products = get_all_products()
    # Return products with their listed prices as strings from the DB.
    return {"products": [{"barcode": bc, "name": p["name"], "price": p["price"], "stock": p["stock"]} for bc, p in products.items()]}

@client_router.post("/order")
async def create_order(order: OrderRequest):
    """
    Client API: Submit a purchase order.
    Middleware has already validated prices against DB.
    This endpoint calculates subtotal, service fee, and total.
    """
    subtotal = 0.0
    
    for item in order.items:
        db_price_float = get_product_price(item.barcode) # Get price as float from DB
        
        if db_price_float is None:
            raise HTTPException(status_code=404, detail=f"Product with barcode {item.barcode} not found.")
        
        # Use the DB price for calculation, as middleware ensures client's price matches.
        subtotal += db_price_float * item.quantity

    service_fee_rate = 0.05
    service_fee = subtotal * service_fee_rate
    total_to_pay = subtotal + service_fee

    return OrderResponse(
        message="Order placed successfully. Thank you for your purchase!",
        subtotal=round(subtotal, 2),
        service_fee=round(service_fee, 2),
        total_to_pay=round(total_to_pay, 2)
    )
