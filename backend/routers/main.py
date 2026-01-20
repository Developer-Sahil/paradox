from fastapi import APIRouter, Depends
from firebase_admin import firestore
from typing import List, Optional

from backend.dependencies import get_db
from backend.models.post import Post

router = APIRouter()

@router.get("/", response_model=List[Post])
async def home(db: firestore.Client = Depends(get_db)):
    """
    Get latest 3 writings for home page
    """
    try:
        # Fetch latest 3 writings from Firestore
        posts_ref = db.collection('writings').order_by(
            'date', 
            direction=firestore.Query.DESCENDING
        ).limit(3)
        docs = posts_ref.stream()
        
        latest_posts = [Post.from_dict(doc) for doc in docs]
        return latest_posts
    except Exception as e:
        # Return empty list if there's an error (e.g., no data yet)
        print(f"Error fetching posts: {e}")
        return []

@router.get("/operator")
async def operator():
    """
    Get operator information
    """
    return {
        "message": "Operator information",
        "profile": "Full-stack engineer. Builder. Writer.",
        "stack": [
            "Python, JavaScript, TypeScript",
            "Flask, Django, React, Node",
            "PostgreSQL, MongoDB, Firebase",
            "AWS, GCP, Docker"
        ],
        "principles": [
            "Ship fast, iterate faster",
            "Code is communication",
            "Systems over solutions",
            "Measure everything"
        ]
    }