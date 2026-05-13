from my_lambda_security_lib.static_analysis import run_static_analysis

if __name__ == "__main__":
    # Run static analysis and print the results
    issues = run_static_analysis()
    if issues:
        print("Static Analysis Issues Detected:", issues)
    else:
        print("No static analysis issues detected.")
