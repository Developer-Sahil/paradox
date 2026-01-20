from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from firebase_admin import firestore

from backend.dependencies import get_db
from backend.models.project import Project

router = APIRouter()

@router.get("/projects", response_model=List[Project])
async def get_all_projects(status: Optional[str] = None, db: firestore.Client = Depends(get_db)):
    projects = Project.get_all(db, status=status)
    return projects

@router.get("/projects/{slug}", response_model=Project)
async def get_project_detail(slug: str, db: firestore.Client = Depends(get_db)):
    project = Project.get_by_slug(db, slug)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
