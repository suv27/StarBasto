
# Simulated database for products
# Prices are in string format to simulate potential variations or currency symbols.
# For comparison, we'll convert to float.

PRODUCTS_DB = {
    "RICE001": {"name": "Rice", "price": "2.50", "stock": 100},
    "SALAMI002": {"name": "Salami", "price": "5.00", "stock": 50},
    "PRESIDENTE003": {"name": "Presidente", "price": "3.75", "stock": 75},
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
