from fastapi import APIRouter, HTTPException
from app.models.employee_model import Employee, EmployeeUpdate
from app.services.employee_service import (
    # SYNC
    add_employee_sync,
    get_all_employees_sync,
    get_employee_sync,
    update_employee_sync,
    delete_employee_sync,

    # ASYNC
    add_employee_async,
    get_all_employees_async,
    get_employee_async,
    update_employee_async,
    delete_employee_async
)

router = APIRouter()

# SYNC ROUTES
@router.post("/employee")
def create_employee_sync(employee: Employee):
    data = employee.dict(exclude_none=True)
    result = add_employee_sync(data)
    if not result.get("success", False):
        raise HTTPException(status_code=400, detail=result.get("message", "Failed to create employee"))
    return result

@router.get("/employees")
def list_employees_sync():
    return get_all_employees_sync()

@router.get("/employee/{emp_id}")
def get_employee_by_id_sync(emp_id: str):
    employee = get_employee_sync(emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/employee/update/{emp_id}")
def update_employee_by_id_sync(emp_id: str, employee: EmployeeUpdate):
    update_data = employee.dict(exclude_none=True)
    success = update_employee_sync(emp_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found or update failed")
    return {"message": "Employee updated successfully"}

@router.delete("/employee/delete/{emp_id}")
def delete_employee_by_id_sync(emp_id: str):
    success = delete_employee_sync(emp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found or delete failed")
    return {"message": "Employee deleted successfully"}


# ASYNC ROUTES
@router.post("/employee_async")
async def create_employee_async(employee: Employee):
    data = employee.dict(exclude_none=True)
    success = await add_employee_async(data)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to create employee")
    return {"message": "Employee created successfully"}

@router.get("/employees_async")
async def list_employees_async():
    return await get_all_employees_async()

@router.get("/employee_async/{emp_id}")
async def get_employee_by_id_async(emp_id: str):
    employee = await get_employee_async(emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/employee_async/update/{emp_id}")
async def update_employee_by_id_async(emp_id: str, employee: EmployeeUpdate):
    update_data = employee.dict(exclude_none=True)
    success = await update_employee_async(emp_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found or update failed")
    return {"message": "Employee updated successfully"}

@router.delete("/employee_async/delete/{emp_id}")
async def delete_employee_by_id_async(emp_id: str):
    success = await delete_employee_async(emp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found or delete failed")
    return {"message": "Employee deleted successfully"}
