def success_response(status_code, message_code, message, error=False, ):
    response_data = {
        "error": error,
        "response": [{
            "status_code": status_code,
            "code": message_code,
            "details": [
                message
            ]
        }]
    }
    return response_data


def error_response(status_code, error_code, message, error=True):
    error_data = {
        "error": error,
        "errors": [{
            "status_code": status_code,
            "error_message": error_code,
            "details": {"message": [message]}
        }]
    }

    return error_data
