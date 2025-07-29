from fastapi import APIRouter
from app.Client.api import router as client_router
from app.Employee.api import router as employee_router
from app.Project.api import router as project_router
from app.Region.api import router as region_router


api_router = APIRouter()
api_router.include_router(client_router)
api_router.include_router(employee_router)
api_router.include_router(project_router)
api_router.include_router(region_router)
