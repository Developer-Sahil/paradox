class Project:
    def __init__(self, id, title, description, demo_url=None, github_url=None, 
                 tech_stack=None, status='active', slug=None):
        self.id = id
        self.title = title
        self.description = description
        self.demo_url = demo_url
        self.github_url = github_url
        self.tech_stack = tech_stack or []
        self.status = status
        self.slug = slug or self._generate_slug(title)
    
    @staticmethod
    def _generate_slug(title):
        return title.lower().replace(' ', '-').replace('/', '-')
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'demo_url': self.demo_url,
            'github_url': self.github_url,
            'tech_stack': self.tech_stack,
            'status': self.status,
            'slug': self.slug
        }
    
    @staticmethod
    def from_dict(id, data):
        return Project(
            id=id,
            title=data.get('title'),
            description=data.get('description'),
            demo_url=data.get('demo_url'),
            github_url=data.get('github_url'),
            tech_stack=data.get('tech_stack', []),
            status=data.get('status', 'active'),
            slug=data.get('slug')
        )
    
    @staticmethod
    def get_all(db, status=None):
        projects_ref = db.collection('projects')
        if status:
            docs = projects_ref.where('status', '==', status).stream()
        else:
            docs = projects_ref.stream()
        return [Project.from_dict(doc.id, doc.to_dict()) for doc in docs]
    
    @staticmethod
    def get_by_id(db, id):
        doc = db.collection('projects').document(id).get()
        if doc.exists:
            return Project.from_dict(doc.id, doc.to_dict())
        return None
    
    @staticmethod
    def get_by_slug(db, slug):
        docs = db.collection('projects').where('slug', '==', slug).limit(1).stream()
        for doc in docs:
            return Project.from_dict(doc.id, doc.to_dict())
        return None