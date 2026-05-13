import os
import subprocess

def run_bandit_analysis(target_directory):
    """
    Run Bandit security analysis on the specified directory and return a list of issues.
    Bandit is a tool designed to find common security issues in Python code.
    """
    try:
        result = subprocess.run(
            ["bandit", "-r", target_directory],
            capture_output=True,
            text=True
        )
        return parse_bandit_output(result.stdout)
    except Exception as e:
        print(f"Error running Bandit analysis: {e}")
        return []

def parse_bandit_output(output):
    """
    Parse the output of Bandit to extract the relevant security issues.
    """
    issues = []
    lines = output.splitlines()
    for line in lines:
        if "Issue:" in line:
            issues.append(line.strip())
    return issues

def run_custom_static_checks(lambda_code_path):
    """
    Run additional custom static checks that are not covered by Bandit.
    """
    # Example check for weak cryptography (just a simple keyword search for demonstration)
    issues = []
    with open(lambda_code_path, "r") as code_file:
        code_content = code_file.read()
        if "md5" in code_content or "sha1" in code_content:
            issues.append("Use of weak cryptography detected (MD5/SHA1). Consider using SHA256 or higher.")
    return issues

def run_static_analysis():
    """
    Run the complete static analysis by combining Bandit and custom checks.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    lambda_code_dir = os.path.join(current_dir, "..")  # Assuming the Lambda code is in the parent directory

    # Run Bandit analysis
    bandit_issues = run_bandit_analysis(lambda_code_dir)

    # Run custom static checks
    custom_issues = run_custom_static_checks(os.path.join(lambda_code_dir, "test_function.py"))

    # Combine all issues
    all_issues = bandit_issues + custom_issues
    return all_issues
