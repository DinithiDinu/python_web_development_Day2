import pytest
from pydantic import ValidationError

from app.core.exceptions import ConflictError, NotFoundError
from app.schemas.schemas import DepartmentCreate, EmployeeCreate
from app.services.department_service import DepartmentService
from app.services.employee_service import EmployeeService


def make_employee(department_id, email="a@mail.com", salary=1000):
    return EmployeeCreate(
        name="Test", email=email, department_id=department_id, salary=salary
    )


def test_service_creates_employee(db_session):
    dept = DepartmentService(db_session).create_department(
        DepartmentCreate(department_name="HR")
    )
    employee = EmployeeService(db_session).create_employee(make_employee(dept.department_id))
    assert employee.employee_id is not None


def test_service_rejects_duplicate_email(db_session):
    dept = DepartmentService(db_session).create_department(
        DepartmentCreate(department_name="HR")
    )
    service = EmployeeService(db_session)
    service.create_employee(make_employee(dept.department_id))
    with pytest.raises(ConflictError):
        service.create_employee(make_employee(dept.department_id))


def test_service_rejects_unknown_department(db_session):
    with pytest.raises(NotFoundError):
        EmployeeService(db_session).create_employee(make_employee(999))


def test_schema_rejects_negative_salary():
    with pytest.raises(ValidationError):
        make_employee(1, salary=-10)