class Product:
    def __init__(self, id, title, description, price, url, active=True, slug=None):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.url = url
        self.active = active
        self.slug = slug or self._generate_slug(title)
    
    @staticmethod
    def _generate_slug(title):
        return title.lower().replace(' ', '-').replace('/', '-')
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'url': self.url,
            'active': self.active,
            'slug': self.slug
        }
    
    @staticmethod
    def from_dict(id, data):
        return Product(
            id=id,
            title=data.get('title'),
            description=data.get('description'),
            price=data.get('price'),
            url=data.get('url'),
            active=data.get('active', True),
            slug=data.get('slug')
        )
    
    @staticmethod
    def get_all(db, active_only=True):
        products_ref = db.collection('products')
        if active_only:
            docs = products_ref.where('active', '==', True).stream()
        else:
            docs = products_ref.stream()
        return [Product.from_dict(doc.id, doc.to_dict()) for doc in docs]
    
    @staticmethod
    def get_by_id(db, id):
        doc = db.collection('products').document(id).get()
        if doc.exists:
            return Product.from_dict(doc.id, doc.to_dict())
        return None
    
    @staticmethod
    def get_by_slug(db, slug):
        docs = db.collection('products').where('slug', '==', slug).limit(1).stream()
        for doc in docs:
            return Product.from_dict(doc.id, doc.to_dict())
        return None