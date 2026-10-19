from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.schemas import DepartmentCreate, DepartmentOut
from app.services.department_service import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departments"])


def get_service(db: Session = Depends(get_db)) -> DepartmentService:
    return DepartmentService(db)


@router.post("", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(data: DepartmentCreate, service: DepartmentService = Depends(get_service)):
    return service.create_department(data)


@router.get("", response_model=List[DepartmentOut])
def list_departments(service: DepartmentService = Depends(get_service)):
    return service.list_departments()