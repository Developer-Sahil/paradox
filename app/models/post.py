from firebase_admin import firestore
from datetime import datetime

class Post:
    def __init__(self, id, title, content, date, tags=None, series=None, slug=None):
        self.id = id
        self.title = title
        self.content = content
        self.date = date
        self.tags = tags or []
        self.series = series
        self.slug = slug or self._generate_slug(title)
    
    @staticmethod
    def _generate_slug(title):
        return title.lower().replace(' ', '-').replace('/', '-')
    
    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'date': self.date,
            'tags': self.tags,
            'series': self.series,
            'slug': self.slug
        }
    
    @staticmethod
    def from_dict(id, data):
        return Post(
            id=id,
            title=data.get('title'),
            content=data.get('content'),
            date=data.get('date'),
            tags=data.get('tags', []),
            series=data.get('series'),
            slug=data.get('slug')
        )
    
    @staticmethod
    def get_all(db):
        posts_ref = db.collection('writings')
        docs = posts_ref.order_by('date', direction=firestore.Query.DESCENDING).stream()
        return [Post.from_dict(doc.id, doc.to_dict()) for doc in docs]
    
    @staticmethod
    def get_by_id(db, id):
        doc = db.collection('writings').document(id).get()
        if doc.exists:
            return Post.from_dict(doc.id, doc.to_dict())
        return None
    
    @staticmethod
    def get_by_slug(db, slug):
        docs = db.collection('writings').where('slug', '==', slug).limit(1).stream()
        for doc in docs:
            return Post.from_dict(doc.id, doc.to_dict())
        return None
    
    @staticmethod
    def get_by_series(db, series):
        docs = db.collection('writings').where('series', '==', series).order_by('date').stream()
        return [Post.from_dict(doc.id, doc.to_dict()) for doc in docs]