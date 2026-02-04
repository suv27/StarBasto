
from typing import Dict, List, Any, Union
from fastapi import HTTPException, Depends, FastAPI
from pydantic import BaseModel, Field
import logging

# Import database functions
from database import (
    get_product_by_barcode,
    get_product_price,
    deduct_stock,
    delete_product,
    mark_product_unavailable,
    update_product_stock,
    get_all_products # Needed for cart details checkout
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Pydantic Models for Cart ---

class CartItem(BaseModel):
    barcode: str
    quantity: int
    # Price will be fetched from DB at checkout/display time, not stored in cart item model here
    # This ensures price consistency with the source of truth.

class Cart(BaseModel):
    items: Dict[str, CartItem] # barcode -> CartItem

# --- In-memory Cart Storage ---
# This is a simplified in-memory cart. In a real application, this would be a database or a more robust session management system.
# We'll simulate a single cart for simplicity, managed globally.
# For multiple users, you'd need a way to associate carts with users (e.g., user ID, session token).

class InMemoryCartManager:
    def __init__(self):
        self.carts: Dict[str, Cart] = {}
        self.default_user_id = "default_user" # For single user simulation

    def get_cart(self, user_id: str = "default_user") -> Cart:
        if user_id not in self.carts:
            self.carts[user_id] = Cart(items={})
        return self.carts[user_id]

    def clear_cart(self, user_id: str = "default_user"):
        if user_id in self.carts:
            self.carts[user_id].items.clear() # Clear items in the existing cart object
            logger.info(f"Cart cleared for user: {user_id}")

# Initialize the cart manager
cart_manager = InMemoryCartManager()

# --- Cart API Endpoints ---

# Dependency to get the current user's cart
def get_current_cart(user_id: str = "default_user") -> Cart:
    """Dependency to provide the current user's cart."""
    return cart_manager.get_cart(user_id)

async def add_item_to_cart(cart: Cart, barcode: str, quantity: int):
    """Adds or updates an item in the cart."""
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive.")

    product = get_product_by_barcode(barcode)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with barcode {barcode} not found.")

    current_stock = product.get("stock", 0)
    
    # Calculate the total quantity if item is already in cart plus the new quantity
    existing_quantity = cart.items.get(barcode).quantity if barcode in cart.items else 0
    new_total_quantity = existing_quantity + quantity
    
    if current_stock < new_total_quantity:
        raise HTTPException(status_code=400, detail=f"Insufficient stock for {product['name']}. Available: {current_stock}. Cannot add {quantity} more.")

    if barcode in cart.items:
        cart.items[barcode].quantity = new_total_quantity
    else:
        cart.items[barcode] = CartItem(barcode=barcode, quantity=quantity)
    
    logger.info(f"Item {barcode} added/updated in cart for user. New quantity: {cart.items[barcode].quantity}")
    return cart

async def remove_item_from_cart(cart: Cart, barcode: str):
    """Removes an item from the cart."""
    if barcode in cart.items:
        del cart.items[barcode]
        logger.info(f"Item {barcode} removed from cart.")
        return True
    return False

async def get_cart_details_for_checkout(cart: Cart) -> Dict[str, Any]:
    """
    Fetches full product details for items in the cart and calculates subtotal.
    This is crucial for checkout to ensure accurate prices and availability are used.
    It also helps in generating the final response format.
    """
    checkout_items_list = []
    subtotal = 0.0
    
    for barcode, cart_item in cart.items.items():
        product = get_product_by_barcode(barcode)
        if not product:
            # This case should ideally be handled when adding to cart, but as a safeguard
            raise HTTPException(status_code=404, detail=f"Product with barcode {barcode} found in cart but not in database.")
        
        db_price_float = get_product_price(barcode)
        if db_price_float is None:
            raise HTTPException(status_code=500, detail=f"Product {barcode} has an invalid price in the database.")
            
        # Re-check stock availability at the moment of checkout
        current_stock = product.get("stock", 0)
        if current_stock < cart_item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product['name']} (barcode: {barcode}). Available: {current_stock}.")
            
        item_total = db_price_float * cart_item.quantity
        subtotal += item_total
        
        checkout_items_list.append({
            "barcode": barcode,
            "name": product["name"],
            "price_per_unit": f"{db_price_float:.2f}", # Use DB price for display/checkout
            "quantity": cart_item.quantity,
            "item_subtotal": f"{item_total:.2f}"
        })
    
    return {"items": checkout_items_list, "subtotal": subtotal}

