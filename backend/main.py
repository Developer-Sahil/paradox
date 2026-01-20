from fastapi import FastAPI

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

app = FastAPI(title="Personal Portfolio API", version="1.0.0")

app.include_router(main_router.router)
app.include_router(writings_router.router)
app.include_router(products_router.router)
app.include_router(projects_router.router)
app.include_router(systems_router.router)
app.include_router(vault_router.router)
app.include_router(arena_router.router)
app.include_router(metrics_router.router)
app.include_router(work_router.router)
app.include_router(admin_router.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI backend!"}
