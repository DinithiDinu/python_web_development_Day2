from pickle import GET
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from httpx import put

app = FastAPI()

employees = [
{
    "employee_id": 1,
    "name": "Tesheena",
    "email": "t@gmail.com",
    "salary": 50000,
    "department id": 2,
    "status": "Active" 
},
{
    "employee_id": 2,
    "name": "Supuni",
    "email": "s@gmail.com",
    "salary": 69000,
    "department id": 1,
    "status": "Active"
},
{
    "employee_id": 3,
    "name": "Dinithi",  
    "email": "d@gmail.com",
    "salary": 80000,
    "department id": 2,
    "status": "Active"
}
]

class EmployeeCreate(BaseModel):
    employee_id: int
    name: str = Field(min_length = 1)
    email: str
    salary: float = Field(gt=0)
    department_id: int
    status: str

# get all employees
@app.get("/employees")
def get_employees(
    department_id: int = None,
    status: str = None,
    min_salary: float = None
):
    result = employees

    if department_id is not None:
        result = [employee for employee in result if employee["department id"] == department_id]

    if status is not None:
        result = [employee for employee in result if employee["status"].lower() == status.lower()]

    if min_salary is not None:
        result = [employee for employee in result if employee["salary"] >= min_salary]

    return result

# get one employee
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["employee_id"] == employee_id:
            return employee

        raise HTTPException(status_code=404, detail="Employee not found")


# POST /employee
@app.post("/employees")
def create_employee(employee: EmployeeCreate):

    for existing_employee in employees:
        if existing_employee["email"] == employee.email:
            raise HTTPException(status_code=400, detail="Employee with this email already exists")
        
    employee_data = employee.model_dump()
    employee_data["employee_id"] = len(employees) + 1

    employees.append(employee_data)
    return {"message": "Employee created successfully", "employee": employee_data}

# PUT - update employee

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeCreate):

    for existing_employee in employees:
        if existing_employee["employee_id"] == employee_id:

            existing_employee["name"] = employee.name
            existing_employee["email"] = employee.email
            existing_employee["salary"] = employee.salary
            existing_employee["department_id"] = employee.department_id
            existing_employee["status"] = employee.status

        return {"message": "Employee updated successfully", "employee": existing_employee}
    raise HTTPException(status_code=404, detail="Employee not found")

# DELETE /employees/{employee_id}

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for employee in employees:
        if employee["employee_id"] == employee_id:
            employees.remove(employee)
            return {"message": "Employee deleted successfully"}

    raise HTTPException(status_code=404, detail="Employee not found")
