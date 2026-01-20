from pydantic import BaseModel
from typing import Optional, List
from firebase_admin import firestore

class VaultItem(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    category: str
    tags: List[str]

    @staticmethod
    def from_dict(source):
        item_dict = source.to_dict()
        item_dict["id"] = source.id
        return VaultItem(**item_dict)

    @staticmethod
    def get_all(db, category: Optional[str] = None):
        vault_ref = db.collection('vault')
        if category:
            vault_ref = vault_ref.where('category', '==', category)
        docs = vault_ref.stream()
        return [VaultItem.from_dict(doc) for doc in docs]

    @staticmethod
    def get_by_id(db, item_id: str):
        doc = db.collection('vault').document(item_id).get()
        if doc.exists:
            return VaultItem.from_dict(doc)
        return None
