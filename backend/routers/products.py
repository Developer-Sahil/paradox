from fastapi import APIRouter, Depends, HTTPException
from typing import List
from firebase_admin import firestore

from backend.dependencies import get_db
from backend.models.product import Product

router = APIRouter()

@router.get("/products", response_model=List[Product])
async def get_all_products(active_only: bool = True, db: firestore.Client = Depends(get_db)):
    products = Product.get_all(db, active_only=active_only)
    return products

@router.get("/products/{slug}", response_model=Product)
async def get_product_detail(slug: str, db: firestore.Client = Depends(get_db)):
    product = Product.get_by_slug(db, slug)
    if not product or (not product.active and active_only):
        raise HTTPException(status_code=404, detail="Product not found or not active")
    return product
