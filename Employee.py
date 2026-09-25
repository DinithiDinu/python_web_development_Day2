class Employee:
    def __init__(self, employee_id, name, email, salary, department, status):
        if salary < 0:
            raise ValueError("Incorrect salary..")


        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.salary = salary
        self.department = department
        self.status = status


    def get_details(self):
        return{
            "Employee Id: ": self.employee_id,
            "Name: ": self.name,
            "email: ": self.email,
            "salary: ": self.salary,
            "department: ": self.department,
            "status: ": self.status
        }

    def calculate_annual_salary(self):
        return self.salary * 12

    def update_salary(self, new_salary):
        if new_salary < 0:
            raise ValueError("Salary must be positive")

        self.salary = new_salary



# Testing 

employee = Employee(
    1,
    "Dinithi",
    "dinithi@mail.com",
    60000,
    "Data Science",
    "Active"
)

print(employee.get_details())
print("Annual Salary: ", employee.calculate_annual_salary())
employee.update_salary(65000)

print("Updated salary: ", employee.salary)
