from fastapi import FastAPI
from middleware import StarDefenseGuard # Ensure this matches your filename
from routes import owner_router, client_router

app = FastAPI()

# IMPORTANT: The middleware must be added BEFORE the routers
app.add_middleware(StarDefenseGuard)

app.include_router(owner_router)
app.include_router(client_router)