from pydantic import BaseModel
from typing import Optional, List
from firebase_admin import firestore

class Tool(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    url: Optional[str]
    category: str

    @staticmethod
    def from_dict(source):
        tool_dict = source.to_dict()
        tool_dict["id"] = source.id
        return Tool(**tool_dict)

    @staticmethod
    def get_all(db):
        tools_ref = db.collection('tools')
        docs = tools_ref.stream()
        return [Tool.from_dict(doc) for doc in docs]

    @staticmethod
    def get_by_id(db, tool_id: str):
        doc = db.collection('tools').document(tool_id).get()
        if doc.exists:
            return Tool.from_dict(doc)
        return None
