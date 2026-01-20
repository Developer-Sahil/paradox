from pydantic import BaseModel
from typing import List, Optional
from firebase_admin import firestore

class Post(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    date: str
    tags: List[str]
    series: Optional[str]
    slug: str

    @staticmethod
    def from_dict(source):
        post_dict = source.to_dict()
        post_dict["id"] = source.id
        return Post(**post_dict)

    @staticmethod
    def get_all(db):
        posts_ref = db.collection('writings').order_by('date', direction=firestore.Query.DESCENDING)
        docs = posts_ref.stream()
        return [Post.from_dict(doc) for doc in docs]
    
    @staticmethod
    def get_by_slug(db, slug: str):
        posts_ref = db.collection('writings').where('slug', '==', slug).limit(1)
        docs = posts_ref.stream()
        for doc in docs:
            return Post.from_dict(doc)
        return None

    @staticmethod
    def get_by_series(db, series_name: str):
        posts_ref = db.collection('writings').where('series', '==', series_name).order_by('date', direction=firestore.Query.DESCENDING)
        docs = posts_ref.stream()
        return [Post.from_dict(doc) for doc in docs]
