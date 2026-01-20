from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import firestore
from pydantic import BaseModel
from typing import List, Optional

from backend.dependencies import get_db

router = APIRouter()

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
    def get_all_posts(db: firestore.Client):
        posts_ref = db.collection('writings').order_by('date', direction=firestore.Query.DESCENDING).limit(3)
        docs = posts_ref.stream()
        return [Post.from_dict(doc) for doc in docs]

@router.get("/", response_model=List[Post])
async def home(db: firestore.Client = Depends(get_db)):
    # Fetch latest 3 writings from Firestore
    latest_posts = Post.get_all_posts(db)
    return latest_posts

@router.get("/operator")
async def operator():
    return {"message": "Operator page data"}
