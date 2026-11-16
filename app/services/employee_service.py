from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.models import Employee, Leave
from app.repositories.department_repository import DepartmentRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.leave_repository import LeaveRepository
from app.schemas.schemas import EmployeeCreate, EmployeeUpdate, LeaveCreate


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
        self.employees = EmployeeRepository(db)
        self.departments = DepartmentRepository(db)
        self.leaves = LeaveRepository(db)

    #  helpers 
    def _commit(self):
        """Commit the transaction; roll back everything if it fails."""
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ConflictError("Duplicate value or invalid reference")
        except Exception:
            self.db.rollback()
            raise

    def _get_or_404(self, employee_id: int) -> Employee:
        employee = self.employees.get_by_id(employee_id)
        if not employee:
            raise NotFoundError(f"Employee {employee_id} not found")
        return employee

    def _check_department(self, department_id: int):
        if not self.departments.get_by_id(department_id):
            raise NotFoundError(f"Department {department_id} does not exist")

    #  employees 
    def create_employee(self, data: EmployeeCreate) -> Employee:
        self._check_department(data.department_id)       # department_id=999 case
        if self.employees.get_by_email(data.email):
            raise ConflictError("Employee with this email already exists")

        employee = Employee(**data.model_dump())
        self.employees.add(employee)
        self._commit()
        self.db.refresh(employee)
        return employee

    def list_employees(self, skip: int = 0, limit: int = 20):
        items, total = self.employees.get_page(skip, limit)
        return {"items": items, "total": total, "skip": skip, "limit": limit}

    def get_employee(self, employee_id: int) -> Employee:
        return self._get_or_404(employee_id)

    def update_employee(self, employee_id: int, data: EmployeeUpdate) -> Employee:
        employee = self._get_or_404(employee_id)
        self._check_department(data.department_id)

        existing = self.employees.get_by_email(data.email)
        if existing and existing.employee_id != employee_id:
            raise ConflictError("Another employee already uses this email")

        for field, value in data.model_dump().items():
            setattr(employee, field, value)
        self._commit()
        self.db.refresh(employee)
        return employee

    def delete_employee(self, employee_id: int):
        employee = self._get_or_404(employee_id)
        self.employees.soft_delete(employee)              # soft delete, not a physical delete
        self._commit()

    # leave 
    def add_leave(self, employee_id: int, data: LeaveCreate) -> Leave:
        self._get_or_404(employee_id)
        leave = Leave(employee_id=employee_id, **data.model_dump())
        self.leaves.add(leave)
        self._commit()
        self.db.refresh(leave)
        return leave

    def get_leaves(self, employee_id: int):
        self._get_or_404(employee_id)
        return self.leaves.get_by_employee(employee_id)