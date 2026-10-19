from sqlalchemy.orm import Session
from app.models.models import Employee


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, employee_id: int):
        return (
            self.db.query(Employee)
            .filter(Employee.employee_id == employee_id, Employee.is_deleted == False)
            .first()
        )

    def get_by_email(self, email: str):
        return self.db.query(Employee).filter(Employee.email == email).first()

    def get_all(self):
        return self.db.query(Employee).filter(Employee.is_deleted == False).all()

    def add(self, employee: Employee):
        self.db.add(employee)

    def soft_delete(self, employee: Employee):
        employee.is_deleted = True