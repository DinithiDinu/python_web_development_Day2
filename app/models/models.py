from datetime import datetime, date

from sqlalchemy import String, Numeric, ForeignKey, Date, DateTime, Boolean, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.database import Base   # adjust to wherever your database.py lives


class Department(Base):
    __tablename__ = "departments"

    department_id: Mapped[int] = mapped_column(primary_key=True)
    department_name: Mapped[str] = mapped_column(String(100), unique=True)

    employees = relationship("Employee", back_populates="department")


class Employee(Base):
    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.department_id"))
    salary: Mapped[float] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(String(20), default="Active")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)  # soft delete

    department = relationship("Department", back_populates="employees")
    leaves = relationship("Leave", back_populates="employee")


class Leave(Base):
    __tablename__ = "leaves"

    leave_id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.employee_id"))
    leave_type: Mapped[str] = mapped_column(String(30))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="Pending")

    employee = relationship("Employee", back_populates="leaves")