from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import main as main_router
from backend.routers import writings as writings_router
from backend.routers import products as products_router
from backend.routers import projects as projects_router
from backend.routers import systems as systems_router
from backend.routers import vault as vault_router
from backend.routers import arena as arena_router
from backend.routers import metrics as metrics_router
from backend.routers import work as work_router
from backend.routers import admin as admin_router

app = FastAPI(
    title="Personal Portfolio API",
    version="1.0.0",
    description="FastAPI backend for personal portfolio website"
)

# CORS Configuration - Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",
        "http://localhost:5000",  # Flask (if still using)
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(main_router.router, tags=["Main"])
app.include_router(writings_router.router, tags=["Writings"])
app.include_router(products_router.router, tags=["Products"])
app.include_router(projects_router.router, tags=["Projects"])
app.include_router(systems_router.router, tags=["Systems"])
app.include_router(vault_router.router, tags=["Vault"])
app.include_router(arena_router.router, tags=["Arena"])
app.include_router(metrics_router.router, tags=["Metrics"])
app.include_router(work_router.router, tags=["Work"])
app.include_router(admin_router.router, tags=["Admin"])

@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint - API health check"""
    return {
        "message": "Welcome to the Personal Portfolio API!",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Root"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}