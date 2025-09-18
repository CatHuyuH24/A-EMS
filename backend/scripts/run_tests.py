#!/usr/bin/env python3
"""
Test runner script for A-EMS backend services.
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse

def run_command(command, cwd=None):
    """Run shell command and return result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}")
        print(f"Exit code: {e.returncode}")
        return False

def discover_test_files():
    """Discover all test files in the project."""
    test_files = []
    
    # Find test files in services
    services_dir = Path("services")
    if services_dir.exists():
        for service_dir in services_dir.iterdir():
            if service_dir.is_dir():
                test_dir = service_dir / "tests"
                if test_dir.exists():
                    test_files.extend(test_dir.rglob("test_*.py"))
                    test_files.extend(test_dir.rglob("*_test.py"))
    
    # Find test files in shared modules
    shared_tests = Path("shared") / "tests"
    if shared_tests.exists():
        test_files.extend(shared_tests.rglob("test_*.py"))
        test_files.extend(shared_tests.rglob("*_test.py"))
    
    # Find test files in api_gateway
    gateway_tests = Path("api_gateway") / "tests"
    if gateway_tests.exists():
        test_files.extend(gateway_tests.rglob("test_*.py"))
        test_files.extend(gateway_tests.rglob("*_test.py"))
    
    return test_files

def run_unit_tests(service=None, verbose=False):
    """Run unit tests."""
    print("Running unit tests...")
    
    if service:
        test_path = f"services/{service}/tests"
        if not Path(test_path).exists():
            print(f"Test directory not found: {test_path}")
            return False
    else:
        test_path = "."
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    cmd.extend([
        "--tb=short",
        "--show-capture=no",
        test_path
    ])
    
    return run_command(" ".join(cmd))

def run_integration_tests():
    """Run integration tests."""
    print("Running integration tests...")
    
    # Integration tests require services to be running
    # This is a placeholder for actual integration test logic
    cmd = [
        "python", "-m", "pytest",
        "-v",
        "--tb=short",
        "-m", "integration"
    ]
    
    return run_command(" ".join(cmd))

def run_lint_checks():
    """Run code linting checks."""
    print("Running lint checks...")
    
    # Install flake8 if needed
    subprocess.run([sys.executable, "-m", "pip", "install", "flake8"], 
                  capture_output=True)
    
    # Run flake8
    return run_command("python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics")

def run_security_checks():
    """Run security checks."""
    print("Running security checks...")
    
    # Install bandit if needed
    subprocess.run([sys.executable, "-m", "pip", "install", "bandit"], 
                  capture_output=True)
    
    # Run bandit security checks
    return run_command("python -m bandit -r . -f json -o bandit-report.json")

def generate_test_report():
    """Generate test coverage report."""
    print("Generating test coverage report...")
    
    # Install coverage if needed
    subprocess.run([sys.executable, "-m", "pip", "install", "coverage"], 
                  capture_output=True)
    
    # Run tests with coverage
    success = run_command("python -m coverage run -m pytest")
    if success:
        run_command("python -m coverage report")
        run_command("python -m coverage html")
        print("Coverage report generated in htmlcov/")
    
    return success

def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run tests for A-EMS backend services")
    parser.add_argument("--service", help="Run tests for specific service")
    parser.add_argument("--unit-only", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration-only", action="store_true", help="Run only integration tests")
    parser.add_argument("--lint", action="store_true", help="Run lint checks")
    parser.add_argument("--security", action="store_true", help="Run security checks")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--all", action="store_true", help="Run all checks")
    
    args = parser.parse_args()
    
    print("A-EMS Backend Test Runner")
    print("=" * 30)
    
    success = True
    
    # Discover tests
    test_files = discover_test_files()
    print(f"Found {len(test_files)} test files")
    
    # Run specific test types
    if args.all or (not any([args.unit_only, args.integration_only, args.lint, args.security, args.coverage])):
        # Run all tests by default
        if not run_unit_tests(args.service, args.verbose):
            success = False
        
        if not args.unit_only:
            if not run_integration_tests():
                success = False
    
    elif args.unit_only:
        if not run_unit_tests(args.service, args.verbose):
            success = False
    
    elif args.integration_only:
        if not run_integration_tests():
            success = False
    
    # Run additional checks
    if args.lint or args.all:
        if not run_lint_checks():
            success = False
    
    if args.security or args.all:
        if not run_security_checks():
            success = False
    
    if args.coverage or args.all:
        if not generate_test_report():
            success = False
    
    print("\n" + "=" * 30)
    if success:
        print("All tests passed successfully!")
        sys.exit(0)
    else:
        print("Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()