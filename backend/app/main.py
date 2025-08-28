from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .routers import products, orders, auth

app = FastAPI(title="Simple Shop API")

origins = [o.strip() for o in os.getenv("ALLOW_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"ok": True, "service": "simple-shop-api"}
