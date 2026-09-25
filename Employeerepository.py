from Employee import Employee

class EmployeeRepository:
    def __init__(self):
        self.employees = {}

    def create(self, employee):
        self.employees[employee.employee_id] = employee

    def get_by_id(self, employee_id):
        return self.employees.get(employee_id)

    def get_all(self):
        return list(self.employees.values())

    def update(self, employee):
        self.employees[employee.employee_id] = employee

    def delete(self, employee_id):
        if employee_id in self.employees:
            del self.employees[employee_id]

