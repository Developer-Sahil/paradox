from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Union

from backend.main import db
from backend.models.metric import Metric

router = APIRouter()

@router.get("/metrics", response_model=List[Metric])
async def get_all_metrics():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    metrics = Metric.get_all(db)
    return metrics

@router.get("/metrics/grouped")
async def get_grouped_metrics() -> Dict[str, List[Metric]]:
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    metrics = Metric.get_all(db)
    
    grouped = {}
    for metric in metrics:
        cat = metric.category or 'general'
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(metric)
    
    return grouped
