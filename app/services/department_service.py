from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.models.models import Department
from app.repositories.department_repository import DepartmentRepository
from app.schemas.schemas import DepartmentCreate


class DepartmentService:
    def __init__(self, db: Session):
        self.db = db
        self.departments = DepartmentRepository(db)

    def create_department(self, data: DepartmentCreate):
        if self.departments.get_by_name(data.department_name):
            raise ConflictError("Department already exists")

        department = Department(department_name=data.department_name)
        self.departments.add(department)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ConflictError("Department already exists")
        self.db.refresh(department)
        return department

    def list_departments(self):
        return self.departments.get_all()