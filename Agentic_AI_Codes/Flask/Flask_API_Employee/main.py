from app.service.employee_service import get_all_employees, get_bench_employees, get_by_project_status
from flask import Flask, jsonify, request
from app.utils.logger import get_logger
from app.utils.decoraters import handle_exceptions, time_execution_logger

# Initialize logger with application name
logger = get_logger('employee_api.main')

app = Flask(__name__)

@app.route("/")
def health_check():
    logger.info(f"API REQUEST: Health check requested from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    return {"Status" : "Employee API is Running as Expected. State = Healthy"}

@app.route("/employees", methods=["GET"])
@time_execution_logger
@handle_exceptions
def fetch_all_employees(): 
    all_emps = get_all_employees()
    return jsonify(all_emps), 200

@time_execution_logger
@app.route("/employees/bench", methods=["GET"])
def fetch_bench_employees():
    log_id = id(request)
    logger.info(f"API REQUEST [{log_id}]: Bench employees endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    bench_emps = get_bench_employees()
    
    logger.info(f"API RESPONSE [{log_id}]: Returning {len(bench_emps)} bench employees with HTTP 200 status")
    return jsonify(bench_emps), 200

@time_execution_logger
@app.route("/employees/active_projects", methods=["GET"])
def fetch_active_project_employees(): 
    log_id = id(request)
    logger.info(f"API REQUEST [{log_id}]: Active projects endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    active_emps = get_by_project_status("active")
    
    logger.info(f"API RESPONSE [{log_id}]: Returning {len(active_emps)} employees with active projects with HTTP 200 status")
    return jsonify(active_emps), 200

@time_execution_logger
@app.route("/employees/completed_projects", methods=["GET"])
def fetch_completed_project_employees(): 
    log_id = id(request)
    logger.info(f"API REQUEST [{log_id}]: Completed projects endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    completed_emps = get_by_project_status("completed")
    
    logger.info(f"API RESPONSE [{log_id}]: Returning {len(completed_emps)} employees with completed projects with HTTP 200 status")
    return jsonify(completed_emps), 200

if __name__ == "__main__":
    logger.info("SERVER STARTUP: Initializing Employee API server")
    logger.info(f"SERVER CONFIG: Debug mode: {app.debug}, Host: 127.0.0.1, Port: 5000")
    

    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.endpoint} [{', '.join(rule.methods)}] {rule}")
    
    logger.info(f"SERVER ROUTES: Available endpoints: {routes}")
    logger.info("SERVER READY: Employee API server is ready to accept requests")
    
    app.run(debug=True)