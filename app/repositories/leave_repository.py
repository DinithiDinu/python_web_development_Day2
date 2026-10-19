from sqlalchemy.orm import Session
from app.models.models import Leave


class LeaveRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, leave: Leave):
        self.db.add(leave)

    def get_by_employee(self, employee_id: int):
        return self.db.query(Leave).filter(Leave.employee_id == employee_id).all()