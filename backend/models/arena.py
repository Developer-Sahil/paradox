from pydantic import BaseModel
from typing import Optional, List
from firebase_admin import firestore

class ArenaPost(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    date: str
    tags: List[str]

    @staticmethod
    def from_dict(source):
        post_dict = source.to_dict()
        post_dict["id"] = source.id
        return ArenaPost(**post_dict)

    @staticmethod
    def get_all(db):
        posts_ref = db.collection('arena').order_by('date', direction=firestore.Query.DESCENDING)
        docs = posts_ref.stream()
        return [ArenaPost.from_dict(doc) for doc in docs]

    @staticmethod
    def get_by_id(db, post_id: str):
        doc = db.collection('arena').document(post_id).get()
        if doc.exists:
            return ArenaPost.from_dict(doc)
        return None
