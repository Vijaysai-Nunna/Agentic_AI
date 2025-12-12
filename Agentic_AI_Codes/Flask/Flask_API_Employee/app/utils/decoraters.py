from functools import wraps
import time
from flask import jsonify, request
from app.utils.logger import get_logger

logger = get_logger('employee_api.decorators')

def time_execution_logger(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        try:

            start_time = time.time()            
            result, status_code =  func(*args, **kwargs)
            end_time = time.time()
            execution_time_ms = round ((end_time - start_time) * 1000,2)

            if isinstance(result,dict):
                result['execution_time_ms'] = execution_time_ms
            else:
                 data = result.get_json()
                 if isinstance(data,list):
                    data = {'data': data, 'execution_time_ms' : execution_time_ms }
                 elif isinstance(data,dict):
                     result['execution_time_ms'] = execution_time_ms
                 else:
                     data = {'data': data, 'execution_time_ms' : execution_time_ms }


            result = jsonify(data)
            return result, status_code
        
        except Exception as e:
            return jsonify({"Error" : str(e) }), 500
    return wrapper


def handle_exceptions(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({"Error" : str(e) }), 500
    return wrapper