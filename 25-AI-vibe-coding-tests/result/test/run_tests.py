#!/usr/bin/env python
"""
run_tests.py - Test Runner for Flask Blog API Tests

This script provides a unified way to run tests with various options:
- Run all tests
- Run only unit tests
- Run only integration tests
- Generate Markdown reports

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run only unit tests
    python run_tests.py --integration      # Run only integration tests
    python run_tests.py --verbose          # Run with verbose output
    python run_tests.py --report           # Generate Markdown report
"""

import subprocess
import sys
import os
import argparse
from datetime import datetime
from pathlib import Path


def get_test_dir():
    """Get the directory where tests are located."""
    return Path(__file__).parent


def run_pytest(test_type: str = "all", verbose: bool = False, generate_report: bool = True) -> int:
    """
    Run pytest with the specified options.
    
    Args:
        test_type: "all", "unit", or "integration"
        verbose: Whether to run with verbose output
        generate_report: Whether to generate a Markdown report
    
    Returns:
        Exit code from pytest
    """
    test_dir = get_test_dir()
    reports_dir = test_dir / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add test directory based on type
    if test_type == "unit":
        cmd.append(str(test_dir / "unit"))
        marker = "-m unit"
    elif test_type == "integration":
        cmd.append(str(test_dir / "integration"))
        marker = "-m integration"
    else:
        cmd.extend([str(test_dir / "unit"), str(test_dir / "integration")])
        marker = None
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-v")  # Always use verbose for better output
    
    # Add marker filter if specified
    if marker:
        cmd.extend(marker.split())
    
    # Timestamp for reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate HTML report
    html_report = reports_dir / f"test_results_{test_type}_{timestamp}.html"
    cmd.extend(["--html", str(html_report), "--self-contained-html"])
    
    # Print header
    print("=" * 70)
    print(f"  Flask Blog API Test Suite")
    print(f"  Test Type: {test_type.upper()}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    # Run pytest and capture output
    process = subprocess.run(
        cmd,
        cwd=str(test_dir),
        capture_output=True,
        text=True
    )
    
    # Print output
    print(process.stdout)
    if process.stderr:
        print(process.stderr, file=sys.stderr)
    
    # Generate Markdown report
    if generate_report:
        md_report = reports_dir / f"test_results_{test_type}_{timestamp}.md"
        generate_markdown_report(
            test_type=test_type,
            stdout=process.stdout,
            stderr=process.stderr,
            exit_code=process.returncode,
            output_file=md_report,
            html_report=html_report
        )
        print(f"\nMarkdown report saved to: {md_report}")
        print(f"HTML report saved to: {html_report}")
    
    return process.returncode


def generate_markdown_report(
    test_type: str,
    stdout: str,
    stderr: str,
    exit_code: int,
    output_file: Path,
    html_report: Path
):
    """Generate a Markdown report from pytest output."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Parse test results from stdout
    passed = 0
    failed = 0
    skipped = 0
    errors = 0
    
    # Look for the summary line (e.g., "5 passed, 2 failed")
    for line in stdout.split("\n"):
        if "passed" in line or "failed" in line or "error" in line:
            if "passed" in line:
                try:
                    # Extract number before "passed"
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if "passed" in part.lower():
                            try:
                                passed = int(parts[i-1].replace(',', ''))
                            except (ValueError, IndexError):
                                pass
                        if "failed" in part.lower():
                            try:
                                failed = int(parts[i-1].replace(',', ''))
                            except (ValueError, IndexError):
                                pass
                        if "skipped" in part.lower():
                            try:
                                skipped = int(parts[i-1].replace(',', ''))
                            except (ValueError, IndexError):
                                pass
                        if "error" in part.lower():
                            try:
                                errors = int(parts[i-1].replace(',', ''))
                            except (ValueError, IndexError):
                                pass
                except Exception:
                    pass
    
    total = passed + failed + skipped + errors
    status = "✅ PASSED" if exit_code == 0 else "❌ FAILED"
    
    # Build the Markdown report
    report = f"""# Test Execution Report

## Summary

| Metric | Value |
|--------|-------|
| **Test Type** | {test_type.upper()} |
| **Execution Time** | {timestamp} |
| **Overall Status** | {status} |
| **Total Tests** | {total} |
| **Passed** | {passed} |
| **Failed** | {failed} |
| **Skipped** | {skipped} |
| **Errors** | {errors} |

## Test Configuration

- **Test Framework**: pytest
- **HTML Report**: [{html_report.name}]({html_report.name})

## Console Output

```
{stdout}
```

"""
    
    if stderr:
        report += f"""## Errors

```
{stderr}
```

"""
    
    if failed > 0 or errors > 0:
        report += """## Failed Tests Analysis

Review the console output above for details on failed tests.
Each failure includes:
- Test name and location
- Expected vs actual values
- Stack trace for debugging

"""
    
    report += f"""---

*Report generated on {timestamp}*
"""
    
    # Write the report
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(
        description="Run Flask Blog API tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run only unit tests
    python run_tests.py --integration      # Run only integration tests
    python run_tests.py -v                 # Run with verbose output
    python run_tests.py --no-report        # Run without generating Markdown report
        """
    )
    
    test_group = parser.add_mutually_exclusive_group()
    test_group.add_argument(
        "--unit", "-u",
        action="store_true",
        help="Run only unit tests"
    )
    test_group.add_argument(
        "--integration", "-i",
        action="store_true",
        help="Run only integration tests"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Run with verbose output"
    )
    
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip Markdown report generation"
    )
    
    args = parser.parse_args()
    
    # Determine test type
    if args.unit:
        test_type = "unit"
    elif args.integration:
        test_type = "integration"
    else:
        test_type = "all"
    
    # Run tests
    exit_code = run_pytest(
        test_type=test_type,
        verbose=args.verbose,
        generate_report=not args.no_report
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
