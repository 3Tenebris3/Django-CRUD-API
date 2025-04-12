from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now, add additional details to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['error_message'] = "A descriptive error occurred. Please review your request."
    
    return response
