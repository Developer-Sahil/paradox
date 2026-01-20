from fastapi import APIRouter, Depends, HTTPException
from typing import List
import markdown
from firebase_admin import firestore

from backend.dependencies import get_db
from backend.models.post import Post

router = APIRouter()

@router.get("/writings", response_model=List[Post])
async def get_all_writings(db: firestore.Client = Depends(get_db)):
    posts = Post.get_all(db)
    return posts

@router.get("/writings/{slug}", response_model=Post)
async def get_writing_detail(slug: str, db: firestore.Client = Depends(get_db)):
    post = Post.get_by_slug(db, slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Convert markdown to HTML
    post.content = markdown.markdown(post.content, extensions=['fenced_code', 'codehilite'])
    
    return post

@router.get("/writings/series/{series_name}", response_model=List[Post])
async def get_writings_by_series(series_name: str, db: firestore.Client = Depends(get_db)):
    posts = Post.get_by_series(db, series_name)
    return posts
