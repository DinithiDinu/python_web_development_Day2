from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import List

#Pagination
class EmployeePage(BaseModel):
    items: List[EmployeeOut]
    total: int
    skip: int
    limit: int

#Department
class DepartmentCreate(BaseModel):
    department_name: str = Field(min_length=1, max_length=100)


class DepartmentOut(BaseModel):
    department_id: int
    department_name: str

    model_config = {"from_attributes": True}


#Employee 
class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    department_id: int
    salary: float = Field(gt=0)
    status: str = "Active"


class EmployeeUpdate(EmployeeCreate):
    pass


class EmployeeOut(BaseModel):
    employee_id: int
    name: str
    email: str
    department_id: int
    salary: float
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


# Leave
class LeaveCreate(BaseModel):
    leave_type: str = Field(min_length=1, max_length=30)
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self


class LeaveOut(BaseModel):
    leave_id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    status: str

    model_config = {"from_attributes": True}

    