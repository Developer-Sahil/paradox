from datetime import datetime

class Metric:
    def __init__(self, id, metric, value, unit, updated=None, category=None):
        self.id = id
        self.metric = metric
        self.value = value
        self.unit = unit
        self.updated = updated or datetime.utcnow().isoformat()
        self.category = category
    
    def to_dict(self):
        return {
            'metric': self.metric,
            'value': self.value,
            'unit': self.unit,
            'updated': self.updated,
            'category': self.category
        }
    
    @staticmethod
    def from_dict(id, data):
        return Metric(
            id=id,
            metric=data.get('metric'),
            value=data.get('value'),
            unit=data.get('unit'),
            updated=data.get('updated'),
            category=data.get('category')
        )
    
    @staticmethod
    def get_all(db, category=None):
        metrics_ref = db.collection('metrics')
        if category:
            docs = metrics_ref.where('category', '==', category).stream()
        else:
            docs = metrics_ref.stream()
        return [Metric.from_dict(doc.id, doc.to_dict()) for doc in docs]
    
    @staticmethod
    def get_by_id(db, id):
        doc = db.collection('metrics').document(id).get()
        if doc.exists:
            return Metric.from_dict(doc.id, doc.to_dict())
        return None