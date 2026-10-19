from sqlalchemy.orm import Session
from app.models.models import Department


class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, department_id: int):
        return self.db.get(Department, department_id)

    def get_by_name(self, name: str):
        return self.db.query(Department).filter(Department.department_name == name).first()

    def get_all(self):
        return self.db.query(Department).all()

    def add(self, department: Department):
        self.db.add(department)