from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AdminLoginRequest(BaseModel):
    id_token: str

class AdminPostCreate(BaseModel):
    title: str
    content: str
    date: Optional[str] = None
    tags: List[str] = []
    series: Optional[str] = None

class AdminPostUpdate(BaseModel):
    title: str
    content: str
    date: Optional[str] = None
    tags: List[str] = []
    series: Optional[str] = None

class AdminProjectCreate(BaseModel):
    title: str
    description: str
    demo_url: Optional[str] = None
    github_url: Optional[str] = None
    tech_stack: List[str] = []
    status: str = "active"

class AdminProjectUpdate(BaseModel):
    title: str
    description: str
    demo_url: Optional[str] = None
    github_url: Optional[str] = None
    tech_stack: List[str] = []
    status: str = "active"

class AdminProductCreate(BaseModel):
    title: str
    description: str
    price: float = 0.0
    url: Optional[str] = None
    active: bool = False

class AdminProductUpdate(BaseModel):
    title: str
    description: str
    price: float = 0.0
    url: Optional[str] = None
    active: bool = False
