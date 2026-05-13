from my_lambda_security_lib.static_analysis import run_static_analysis


def test_static_analysis_runs():
    issues = run_static_analysis()
    # Should return a list (even if empty)
    assert isinstance(issues, list)


def test_static_analysis_detects_issues():
    issues = run_static_analysis()
    # Your library should flag MD5 and eval() in test_function.py
    assert len(issues) > 0
