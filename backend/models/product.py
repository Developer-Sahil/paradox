from pydantic import BaseModel
from typing import Optional, List
from firebase_admin import firestore

class Product(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    price: float
    url: Optional[str]
    active: bool
    slug: str

    @staticmethod
    def from_dict(source):
        product_dict = source.to_dict()
        product_dict["id"] = source.id
        return Product(**product_dict)

    @staticmethod
    def get_all(db, active_only: bool = False):
        products_ref = db.collection('products')
        if active_only:
            products_ref = products_ref.where('active', '==', True)
        docs = products_ref.stream()
        return [Product.from_dict(doc) for doc in docs]

    @staticmethod
    def get_by_slug(db, slug: str):
        products_ref = db.collection('products').where('slug', '==', slug).limit(1)
        docs = products_ref.stream()
        for doc in docs:
            return Product.from_dict(doc)
        return None
