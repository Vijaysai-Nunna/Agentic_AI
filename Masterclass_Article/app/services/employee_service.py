from app.db.mongodb import sync_collection, async_collection 
from app.models.employee_model import Employee, EmployeeUpdate
from app.utils.logger import logger

#SYNC CRUD OPERATIONS
def add_employee_sync(data: dict):
    emp_id = data.get("emp_id")
    if emp_id and sync_collection.find_one({"_id": emp_id}):
        logger.warning(f"Create failed: Employee ID {emp_id} already exists")
        return {"success": False, "message": "Employee already exists", "employee_id": emp_id}
    if "emp_id" in data:
        data["_id"] = data.pop("emp_id")
    sync_collection.insert_one(data)
    logger.info(f"Created new employee: {data.get('_id')}")
    return {"success": True, "message": "Employee created successfully", "employee_id": emp_id or str(data["_id"])}

def get_all_employees_sync():
    employees = []
    for doc in sync_collection.find({}):
        doc["emp_id"] = doc.pop("_id")
        employees.append(doc)
    logger.info("Fetched all employees (sync)")
    return employees

def get_employee_sync(emp_id: str):
    employee = sync_collection.find_one({"_id": emp_id})
    if not employee:
        logger.warning(f"Employee with ID {emp_id} not found.")
        return {"Eror": "Employee not found", "employee_id": emp_id}
    employee["emp_id"] = employee.pop("_id")
    logger.info(f"Fetched employee with ID {emp_id} (sync).")
    return employee

def update_employee_sync(emp_id: str, data: dict):
    result = sync_collection.update_one({"_id": emp_id}, {"$set": data})
    if result.matched_count == 0:
        logger.error(f"Update failed: Employee ID {emp_id} not found")
        return {"success": False, "message": "Employee not found", "employee_id": emp_id}
    logger.info(f"Updated employee: {emp_id}")
    return {"success": True, "message": "Employee updated successfully", "employee_id": emp_id}

def delete_employee_sync(emp_id: str):
    result = sync_collection.delete_one({"_id": emp_id})
    if result.deleted_count == 0:
        logger.error(f"Delete failed: Employee ID {emp_id} not found")
        return {"success": False, "message": "Employee not found", "employee_id": emp_id}
    logger.info(f"Deleted employee: {emp_id}")
    return {"success": True, "message": "Employee deleted successfully", "employee_id": emp_id}

#ASYNC CRUD OPERATIONS

async def add_employee_async(data: dict):
    emp_id = data.get("emp_id")
    if emp_id:
        existing = await async_collection.find_one({"_id": emp_id})
        if existing:
            logger.warning(f"Create failed: Employee ID {emp_id} already exists")
            return {"success": False, "message": "Employee already exists", "employee_id": emp_id}
        data["_id"] = data.pop("emp_id")
    await async_collection.insert_one(data)
    logger.info(f"Created new employee: {emp_id or data.get('_id')}")
    return {"success": True, "message": "Employee created successfully", "employee_id": emp_id or str(data["_id"])}

async def get_all_employees_async():
    employees = []
    cursor = async_collection.find({})
    async for doc in cursor:
        doc["emp_id"] = doc.pop("_id")
        employees.append(doc)
    logger.info("Fetched all employees (async)")
    return employees

async def get_employee_async(emp_id: str):
    employee = await async_collection.find_one({"_id": emp_id})
    if not employee:
        logger.warning(f"Get failed: Employee ID {emp_id} not found")
        return {"Error": "Employee not found", "employee_id": emp_id}
    employee["emp_id"] = employee.pop("_id")
    logger.info(f"Fetched employee: {emp_id}")
    return employee

async def update_employee_async(emp_id: str, update_data: dict):
    result = await async_collection.update_one({"_id": emp_id}, {"$set": update_data})
    if result.matched_count == 0:
        logger.warning(f"Update failed: Employee ID {emp_id} not found")
        return {"success": False, "message": "Employee not found", "employee_id": emp_id}
    logger.info(f"Updated employee: {emp_id}")
    return {"success": True, "message": "Employee updated successfully", "employee_id": emp_id}

async def delete_employee_async(emp_id: str):
    result = await async_collection.delete_one({"_id": emp_id})
    if result.deleted_count == 0:
        logger.warning(f"Delete failed: Employee ID {emp_id} not found")
        return {"success": False, "message": "Employee not found", "employee_id": emp_id}
    logger.info(f"Deleted employee: {emp_id}")
    return {"success": True, "message": "Employee deleted successfully", "employee_id": emp_id}
