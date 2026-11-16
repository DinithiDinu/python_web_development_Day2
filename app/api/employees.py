from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.schemas import (
    EmployeeCreate, EmployeeOut, EmployeeUpdate, LeaveCreate, LeaveOut,
)
from app.services.employee_service import EmployeeService
from app.schemas.schemas import EmployeePage

router = APIRouter(prefix="/employees", tags=["Employees"])


def get_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


@router.post("", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(data: EmployeeCreate, service: EmployeeService = Depends(get_service)):
    return service.create_employee(data)


@router.get("", response_model=List[EmployeeOut])
def list_employees(service: EmployeeService = Depends(get_service)):
    return service.list_employees()


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, service: EmployeeService = Depends(get_service)):
    return service.get_employee(employee_id)


@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, data: EmployeeUpdate,
                    service: EmployeeService = Depends(get_service)):
    return service.update_employee(employee_id, data)


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, service: EmployeeService = Depends(get_service)):
    service.delete_employee(employee_id)
    return {"message": "Employee deleted successfully"}


@router.post("/{employee_id}/leave", response_model=LeaveOut, status_code=status.HTTP_201_CREATED)
def add_leave(employee_id: int, data: LeaveCreate,
              service: EmployeeService = Depends(get_service)):
    return service.add_leave(employee_id, data)


@router.get("/{employee_id}/leave", response_model=List[LeaveOut])
def get_leaves(employee_id: int, service: EmployeeService = Depends(get_service)):
    return service.get_leaves(employee_id)


