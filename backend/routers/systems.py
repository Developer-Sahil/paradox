from fastapi import APIRouter, HTTPException
from typing import List

from firebase_admin import firestore
from backend.dependencies import get_db
from backend.models.tool import Tool

router = APIRouter()

@router.get("/systems", response_model=List[Tool])
async def get_all_tools(db: firestore.Client = Depends(get_db)):
    tools = Tool.get_all(db)
    return tools

@router.get("/systems/{tool_id}", response_model=Tool)
async def get_tool_detail(tool_id: str, db: firestore.Client = Depends(get_db)):
    tool = Tool.get_by_id(db, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool
