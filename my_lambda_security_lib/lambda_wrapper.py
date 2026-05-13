from .static_analysis import run_static_analysis
from .dynamic_monitor import start_dynamic_monitoring, stop_dynamic_monitoring

def secure_lambda(lambda_handler):
    def wrapper(event, context):
        # Run static analysis first
        issues = run_static_analysis()
        if issues:
            print("Static Analysis Issues Detected:", issues)

        # Start dynamic monitoring after static analysis
        start_dynamic_monitoring()

        try:
            # Execute the original lambda function
            result = lambda_handler(event, context)
        finally:
            # Stop dynamic monitoring after the function execution
            stop_dynamic_monitoring()

        return result

    return wrapper
