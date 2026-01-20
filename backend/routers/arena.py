from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
import markdown

from firebase_admin import firestore
from backend.dependencies import get_db
from backend.models.arena import ArenaPost

router = APIRouter()

@router.get("/arena", response_model=List[ArenaPost])
async def get_all_arena_posts(db: firestore.Client = Depends(get_db)):
    posts = ArenaPost.get_all(db)
    return posts

@router.get("/arena/{post_id}", response_model=ArenaPost)
async def get_arena_post_detail(post_id: str, db: firestore.Client = Depends(get_db)):
    post = ArenaPost.get_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Arena post not found")
    
    post.content = markdown.markdown(post.content, extensions=['fenced_code', 'codehilite'])
    
    return post
