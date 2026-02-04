# Simulated database for products
# Prices are in string format to simulate potential variations or currency symbols.
# For comparison, we'll convert to float.

PRODUCTS_DB = {
    "RICE001": {"name": "Rice", "price": "2.50", "stock": 100},
    "SALAMI002": {"name": "Salami", "price": "5.00", "stock": 50},
    "PRESIDENTE003": {"name": "Presidente", "price": "3.75", "stock": 75},
}

def get_product_by_barcode(barcode: str) -> Dict[str, Any] | None:
    """Retrieves a product by its barcode."""
    return PRODUCTS_DB.get(barcode)

def get_all_products() -> Dict[str, Dict[str, Any]]:
    """Retrieves all products, potentially filtering out out-of-stock items if desired for client view."""
    return PRODUCTS_DB

def update_product_details(barcode: str, name: str, price: str, stock_count: int) -> bool:
    """Updates or adds a product's details. Overwrites existing item if barcode matches."""
    try:
        # Validate price format early
        float(price)
    except ValueError:
        raise ValueError(f"Invalid price format: {price}. Price must be a number.")
        
    PRODUCTS_DB[barcode] = {
        "name": name,
        "price": price,
        "stock": stock_count
    }
    return True

def update_product_stock(barcode: str, quantity_change: int) -> bool:
    """Updates the stock of a product. quantity_change can be positive or negative."""
    product = PRODUCTS_DB.get(barcode)
    if not product:
        return False # Product not found
    
    new_stock = product["stock"] + quantity_change
    if new_stock < 0:
        # Do not allow stock to go below zero
        return False
        
    product["stock"] = new_stock
    return True

def deduct_stock(barcode: str, quantity: int) -> bool:
    """Deducts stock for an item. Returns True if successful, False otherwise."""
    product = PRODUCTS_DB.get(barcode)
    if not product:
        return False # Product not found
    
    if product["stock"] >= quantity:
        product["stock"] -= quantity
        return True
    else:
        return False # Insufficient stock

def delete_product(barcode: str) -> bool:
    """Removes a product from the database."""
    if barcode in PRODUCTS_DB:
        del PRODUCTS_DB[barcode]
        return True
    return False

def get_product_price(barcode: str) -> float | None:
    """Retrieves the product price as a float, or None if not found or invalid."""
    product = PRODUCTS_DB.get(barcode)
    if product:
        try:
            return float(product["price"])
        except ValueError:
            return None
    return None

# Helper for owner to mark item as unavailable (set stock to 0)
def mark_product_unavailable(barcode: str) -> bool:
    product = PRODUCTS_DB.get(barcode)
    if product:
        product["stock"] = 0
        return True
    return False
