
# Simulated database for products
# Prices are in string format to simulate potential variations or currency symbols.
# For comparison, we'll convert to float.

orders_db = {} 
owners_db = {} 
PRODUCTS_DB = {
    "RICE001": {"name": "Rice (1lb)", "price": 2.50, "stock": 100},
    "SALAMI002": {"name": "Salami", "price": 5.00, "stock": 50},
    "PRESIDENTE003": {"name": "Presidente", "price": 3.75, "stock": 75},
    "BRUGAL001": {"name": "Brugal Leyenda", "price": 25.50, "stock": 20} # Add this!
}

def get_product_by_barcode(barcode: str):
    return PRODUCTS_DB.get(barcode)

def update_product_stock(barcode: str, new_stock: int):
    if barcode in PRODUCTS_DB:
        PRODUCTS_DB[barcode]["stock"] = new_stock
        return True
    return False

def update_product_details(barcode: str, name: str, price: str, stock_count: int):
    # Overwrites existing item if barcode matches
    PRODUCTS_DB[barcode] = {
        "name": name,
        "price": price,
        "stock": stock_count
    }
    return True

def get_all_products():
    return PRODUCTS_DB

def get_product_price(barcode: str) -> float | None:
    product = PRODUCTS_DB.get(barcode)
    if product:
        try:
            return float(product["price"])
        except ValueError:
            return None
    return None

def search_products(query: str):
    """Search for products by name (case-insensitive)."""
    products = get_all_products() # Using your existing function
    results = []
    for bc, details in products.items():
        if query.lower() in details['name'].lower():
            results.append({"barcode": bc, **details})
    return results

def update_order_status(order_id: str, new_status: str):
    """Updates status: 'pending', 'in_progress', 'out_for_delivery', 'delivered'."""
    if order_id in orders_db:
        orders_db[order_id]["status"] = new_status
        return True
    return False

def register_owner(owner_id: str, shop_name: str, location: str):
    owners_db[owner_id] = {
        "shop_name": shop_name,
        "location": location,
        "verified": True
    }
    return True

def register_owner(owner_id: str, shop_name: str, location: str):
    owners_db[owner_id] = {
        "shop_name": shop_name,
        "location": location,
        "verified": True,
        "joined_date": "2026-02-02"
    }
    return owners_db[owner_id]