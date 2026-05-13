import sys
import time
import os
import psutil
import threading
import requests

# Global variables to store metrics
execution_times = {}
function_call_count = {}
cpu_usage = []
memory_usage = []
network_requests = []
file_operations = []
resource_monitoring_active = True
start_time = None
end_time = None
call_depth = 0
max_call_depth = 0

def trace_calls(frame, event, arg):
    """Trace function calls and return time spent in each function."""
    global call_depth, max_call_depth
    if event == 'call':
        function_name = frame.f_code.co_name
        execution_times[function_name] = time.perf_counter()
        function_call_count[function_name] = function_call_count.get(function_name, 0) + 1
        call_depth += 1
        max_call_depth = max(max_call_depth, call_depth)
        print(f"Function call: {function_name}, Current depth: {call_depth}")
    elif event == 'return':
        function_name = frame.f_code.co_name
        if function_name in execution_times:
            elapsed_time = time.perf_counter() - execution_times[function_name]
            execution_times[function_name] = elapsed_time
            print(f"Function return: {function_name}, Time taken: {elapsed_time:.6f} seconds")
        call_depth -= 1
    return trace_calls

def monitor_resources():
    """Monitor CPU and memory usage during the function execution."""
    global resource_monitoring_active
    process = psutil.Process(os.getpid())  # Get the current process

    # Initial baseline call to set up the monitoring
    process.cpu_percent(interval=None)

    while resource_monitoring_active:
        cpu_percent = process.cpu_percent(interval=None)  # Get the CPU usage since the last call
        memory_info = process.memory_percent()
        cpu_usage.append(cpu_percent)
        memory_usage.append(memory_info)
        print(f"CPU Usage: {cpu_percent:.2f}%, Memory Usage: {memory_info:.2f}%")
        time.sleep(0)  # Yield thread, but immediately resume to capture continuous data

def start_dynamic_monitoring():
    global start_time
    print("Starting dynamic monitoring...")
    start_time = time.time()  # Record the start time

    # Start resource monitoring in a separate thread
    resource_monitor_thread = threading.Thread(target=monitor_resources)
    resource_monitor_thread.daemon = True
    resource_monitor_thread.start()

    # Start tracing function calls
    sys.settrace(trace_calls)

def stop_dynamic_monitoring():
    global resource_monitoring_active, end_time
    sys.settrace(None)
    resource_monitoring_active = False  # Stop resource monitoring
    end_time = time.time()  # Record the end time
    print("Dynamic monitoring stopped.")

    # Output the detailed summary
    output_detailed_summary()

def monitor_network_calls():
    """Monkey-patch the requests module to log all network requests."""
    original_get = requests.get

    def patched_get(*args, **kwargs):
        request_info = {
            'url': args[0],
            'method': 'GET',
            'status_code': None,
            'data_sent': len(kwargs.get('data', b'')),
            'data_received': 0
        }
        response = original_get(*args, **kwargs)
        request_info['status_code'] = response.status_code
        request_info['data_received'] = len(response.content)
        network_requests.append(request_info)
        print(f"Network request made to: {args[0]}, Status: {response.status_code}")
        return response

    requests.get = patched_get

def monitor_file_operations():
    """Monitor file operations by monkey-patching the built-in open function."""
    original_open = open

    def patched_open(*args, **kwargs):
        file_info = {
            'file_name': args[0],
            'mode': kwargs.get('mode', 'r')
        }
        file_operations.append(file_info)
        print(f"File operation: open, File: {args[0]}, Mode: {file_info['mode']}")
        return original_open(*args, **kwargs)

    __builtins__['open'] = patched_open

def output_detailed_summary():
    """Output a detailed summary of all the collected metrics."""
    print("\n--- Detailed Summary ---")

    # Total execution time
    total_execution_time = end_time - start_time
    print(f"Total Execution Time: {total_execution_time:.6f} seconds")

    # Function execution times
    print("\nFunction Execution Times:")
    for function_name, elapsed_time in execution_times.items():
        print(f"- {function_name}: {elapsed_time:.6f} seconds")

    # Function call counts
    print("\nFunction Call Counts:")
    for function_name, count in function_call_count.items():
        print(f"- {function_name}: {count} calls")

    # Maximum call depth
    print(f"\nMaximum Function Call Depth: {max_call_depth}")

    # CPU usage stats
    if cpu_usage:
        avg_cpu_usage = sum(cpu_usage) / len(cpu_usage)
        peak_cpu_usage = max(cpu_usage)
    else:
        avg_cpu_usage = peak_cpu_usage = 0
    print(f"\nAverage CPU Usage: {avg_cpu_usage:.2f}%")
    print(f"Peak CPU Usage: {peak_cpu_usage:.2f}%")

    # Memory usage stats
    if memory_usage:
        avg_memory_usage = sum(memory_usage) / len(memory_usage)
        peak_memory_usage = max(memory_usage)
    else:
        avg_memory_usage = peak_memory_usage = 0
    print(f"Average Memory Usage: {avg_memory_usage:.2f}%")
    print(f"Peak Memory Usage: {peak_memory_usage:.2f}%")

    # Network requests
    total_data_sent = sum(req['data_sent'] for req in network_requests)
    total_data_received = sum(req['data_received'] for req in network_requests)
    print("\nNetwork Requests:")
    if network_requests:
        for req in network_requests:
            print(f"- URL: {req['url']}, Method: {req['method']}, Status: {req['status_code']}, Data Sent: {req['data_sent']} bytes, Data Received: {req['data_received']} bytes")
    else:
        print("- No network requests made.")
    print(f"Total Data Sent: {total_data_sent} bytes")
    print(f"Total Data Received: {total_data_received} bytes")

    # File operations
    print("\nFile Operations:")
    if file_operations:
        for file_op in file_operations:
            print(f"- File: {file_op['file_name']}, Mode: {file_op['mode']}")
    else:
        print("- No file operations performed.")

    print("\n--- End of Summary ---")

# Apply additional monitoring
monitor_network_calls()
monitor_file_operations()
