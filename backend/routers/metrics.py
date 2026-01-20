from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Union
from firebase_admin import firestore

from backend.dependencies import get_db
from backend.models.metric import Metric

router = APIRouter()

@router.get("/metrics", response_model=List[Metric])
async def get_all_metrics(db: firestore.Client = Depends(get_db)):
    metrics = Metric.get_all(db)
    return metrics

@router.get("/metrics/grouped")
async def get_grouped_metrics(db: firestore.Client = Depends(get_db)) -> Dict[str, List[Metric]]:
    metrics = Metric.get_all(db)
    
    grouped = {}
    for metric in metrics:
        cat = metric.category or 'general'
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(metric)
    
    return grouped
