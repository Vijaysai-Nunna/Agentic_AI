from datetime import datetime
from app.model.project import Project

class Employee:
    def __init__(self, emp_id, name, department, salary, designation, location, dob, projects):
        self.emp_id =  emp_id
        self.name = name 
        self.department = department
        self.salary = salary
        self.designation =  designation
        self.location = location
        self.dob = dob
        self.projects = [ Project(**p) for p in projects]

    def is_on_bench(self):
        return len(self.projects) == 0 

    def has_project_with_status(self, status):
        return any(p.status == status for p in self.projects)
    
    def get_age(self):
        birth_date = datetime.strptime(self.dob, "%Y-%m-%d")
        return (datetime.now() - birth_date).days // 365
    
    def to_dict(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "department": self.department,
            "salary": self.salary,
            "designation": self.designation,
            "location": self.location,
            "dob": self.dob,
            "age": self.get_age(), 
            "projects": [p.to_dict() for p in self.projects] 
        }