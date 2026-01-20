from fastapi import APIRouter

router = APIRouter()

@router.get("/work")
async def get_work_info():
    return {"message": "Work page data"}
