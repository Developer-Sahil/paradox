from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth, firestore
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

from backend.main import db
from backend.models.admin import AdminLoginRequest, AdminPostCreate, AdminPostUpdate, AdminProjectCreate, AdminProjectUpdate, AdminProductCreate, AdminProductUpdate
from backend.models.post import Post
from backend.models.product import Product
from backend.models.project import Project

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

# Dependency to get the current user
async def get_current_user(id_token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/admin/login")
async def admin_login(request: AdminLoginRequest):
    try:
        decoded_token = auth.verify_id_token(request.id_token)
        # For now, just return a success message. Session management will be handled by the frontend.
        return {"success": True, "message": "Successfully authenticated"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid authentication credentials: {e}")

@router.post("/admin/logout")
async def admin_logout():
    # Frontend will handle token removal. Here we just confirm a successful 'logout' action.
    return {"success": True, "message": "Logged out successfully"}

@router.get("/admin/dashboard")
async def admin_dashboard(current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    writings_count = len(list(db.collection('writings').stream()))
    projects_count = len(list(db.collection('projects').stream()))
    products_count = len(list(db.collection('products').stream()))
    
    return {
        "writings_count": writings_count,
        "projects_count": projects_count,
        "products_count": products_count
    }

# Writings Management
@router.get("/admin/writings", response_model=List[Post])
async def admin_writings_list(current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    docs = db.collection('writings').order_by('date', direction=firestore.Query.DESCENDING).stream()
    writings = [Post.from_dict(doc) for doc in docs]
    return writings

@router.post("/admin/writings", status_code=status.HTTP_201_CREATED)
async def admin_writings_new(post_data: AdminPostCreate, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    slug = post_data.title.lower().replace(' ', '-').replace('/', '-')
    data = post_data.dict(exclude_unset=True)
    data['slug'] = slug
    data['date'] = data.get('date') or datetime.utcnow().isoformat()
    
    # Ensure tags is a list of strings
    if 'tags' in data and not isinstance(data['tags'], list):
        data['tags'] = [t.strip() for t in data['tags'].split(',') if t.strip()]

    doc_ref = db.collection('writings').add(data)
    return {"id": doc_ref[1].id, **data}

@router.get("/admin/writings/{id}", response_model=Post)
async def admin_writings_edit_get(id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    doc = db.collection('writings').document(id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Writing not found")
    return Post.from_dict(doc)

@router.put("/admin/writings/{id}", response_model=Post)
async def admin_writings_edit_put(id: str, post_data: AdminPostUpdate, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    doc_ref = db.collection('writings').document(id)
    
    slug = post_data.title.lower().replace(' ', '-').replace('/', '-')
    data = post_data.dict(exclude_unset=True)
    data['slug'] = slug
    data['date'] = data.get('date') or datetime.utcnow().isoformat()

    if 'tags' in data and not isinstance(data['tags'], list):
        data['tags'] = [t.strip() for t in data['tags'].split(',') if t.strip()]

    doc_ref.update(data)
    updated_doc = doc_ref.get()
    return Post.from_dict(updated_doc)

@router.delete("/admin/writings/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_writings_delete(id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    db.collection('writings').document(id).delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Projects Management
@router.get("/admin/projects", response_model=List[Project])
async def admin_projects_list(current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    docs = db.collection('projects').stream()
    projects = [Project.from_dict(doc) for doc in docs]
    return projects

@router.post("/admin/projects", status_code=status.HTTP_201_CREATED)
async def admin_projects_new(project_data: AdminProjectCreate, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    slug = project_data.title.lower().replace(' ', '-').replace('/', '-')
    data = project_data.dict(exclude_unset=True)
    data['slug'] = slug

    if 'tech_stack' in data and not isinstance(data['tech_stack'], list):
        data['tech_stack'] = [t.strip() for t in data['tech_stack'].split(',') if t.strip()]

    doc_ref = db.collection('projects').add(data)
    return {"id": doc_ref[1].id, **data}

@router.get("/admin/projects/{id}", response_model=Project)
async def admin_projects_edit_get(id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    doc = db.collection('projects').document(id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Project not found")
    return Project.from_dict(doc)

@router.put("/admin/projects/{id}", response_model=Project)
async def admin_projects_edit_put(id: str, project_data: AdminProjectUpdate, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    doc_ref = db.collection('projects').document(id)
    
    slug = project_data.title.lower().replace(' ', '-').replace('/', '-')
    data = project_data.dict(exclude_unset=True)
    data['slug'] = slug

    if 'tech_stack' in data and not isinstance(data['tech_stack'], list):
        data['tech_stack'] = [t.strip() for t in data['tech_stack'].split(',') if t.strip()]

    doc_ref.update(data)
    updated_doc = doc_ref.get()
    return Project.from_dict(updated_doc)

@router.delete("/admin/projects/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_projects_delete(id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    db.collection('projects').document(id).delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Products Management
@router.get("/admin/products", response_model=List[Product])
async def admin_products_list(current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    docs = db.collection('products').stream()
    products = [Product.from_dict(doc) for doc in docs]
    return products

@router.post("/admin/products", status_code=status.HTTP_201_CREATED)
async def admin_products_new(product_data: AdminProductCreate, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    slug = product_data.title.lower().replace(' ', '-').replace('/', '-')
    data = product_data.dict(exclude_unset=True)
    data['slug'] = slug

    doc_ref = db.collection('products').add(data)
    return {"id": doc_ref[1].id, **data}

@router.get("/admin/products/{id}", response_model=Product)
async def admin_products_edit_get(id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    doc = db.collection('products').document(id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product.from_dict(doc)

@router.put("/admin/products/{id}", response_model=Product)
async def admin_products_edit_put(id: str, product_data: AdminProductUpdate, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    doc_ref = db.collection('products').document(id)
    
    slug = product_data.title.lower().replace(' ', '-').replace('/', '-')
    data = product_data.dict(exclude_unset=True)
    data['slug'] = slug

    doc_ref.update(data)
    updated_doc = doc_ref.get()
    return Product.from_dict(updated_doc)

@router.delete("/admin/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_products_delete(id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    db.collection('products').document(id).delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
