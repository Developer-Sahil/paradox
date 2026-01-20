from pydantic import BaseModel
from typing import Optional
from firebase_admin import firestore

class Metric(BaseModel):
    id: Optional[str] = None
    metric: str
    value: str | float # Changed to allow both string and float
    unit: str
    updated: str
    category: str

    @staticmethod
    def from_dict(source):
        metric_dict = source.to_dict()
        metric_dict["id"] = source.id
        return Metric(**metric_dict)

    @staticmethod
    def get_all(db):
        metrics_ref = db.collection('metrics')
        docs = metrics_ref.stream()
        return [Metric.from_dict(doc) for doc in docs]
