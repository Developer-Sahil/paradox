from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import markdown

from firebase_admin import firestore
from backend.dependencies import get_db
from backend.models.vault import VaultItem

router = APIRouter()

@router.get("/vault", response_model=List[VaultItem])
async def get_all_vault_items(category: Optional[str] = Query(None), db: firestore.Client = Depends(get_db)):
    items = VaultItem.get_all(db, category=category)
    return items

@router.get("/vault/categories")
async def get_vault_categories(db: firestore.Client = Depends(get_db)):
    docs = db.collection('vault').stream()
    categories = set()
    for doc in docs:
        data = doc.to_dict()
        if data.get('category'):
            categories.add(data['category'])
    return sorted(list(categories))

@router.get("/vault/{item_id}", response_model=VaultItem)
async def get_vault_item_detail(item_id: str, db: firestore.Client = Depends(get_db)):
    item = VaultItem.get_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Vault item not found")
    
    item.content = markdown.markdown(item.content, extensions=['fenced_code', 'codehilite'])
    
    return item
