from pydantic import BaseModel
from typing import Optional, List
from firebase_admin import firestore

class Project(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    demo_url: Optional[str]
    github_url: Optional[str]
    tech_stack: List[str]
    status: str
    slug: str

    @staticmethod
    def from_dict(source):
        project_dict = source.to_dict()
        project_dict["id"] = source.id
        return Project(**project_dict)

    @staticmethod
    def get_all(db, status: Optional[str] = None):
        projects_ref = db.collection('projects')
        if status:
            projects_ref = projects_ref.where('status', '==', status)
        docs = projects_ref.stream()
        return [Project.from_dict(doc) for doc in docs]

    @staticmethod
    def get_by_slug(db, slug: str):
        projects_ref = db.collection('projects').where('slug', '==', slug).limit(1)
        docs = projects_ref.stream()
        for doc in docs:
            return Project.from_dict(doc)
        return None
