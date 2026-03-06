#!/usr/bin/env python
"""
run_tests.py - Selenium E2E Test Runner for Flask Blog Admin UI

This script provides a unified way to run E2E tests with various options:
- Run all tests or specific markers
- Headless or visible browser mode
- Generate Markdown and HTML reports

Usage:
    python run_tests.py                      # Run all tests (visible browser)
    python run_tests.py --headless           # Run all tests in headless mode
    python run_tests.py --smoke              # Run only smoke tests
    python run_tests.py --verbose            # Run with verbose output
    python run_tests.py --no-report          # Skip Markdown report generation

Requirements:
    - Chrome browser installed
    - Flask Blog API running at http://localhost:5000
    - Dependencies: pip install -r requirements.txt
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


def run_pytest(
    test_type: str = "all",
    headless: bool = False,
    verbose: bool = True,
    generate_report: bool = True,
    base_url: str = "http://localhost:5000"
) -> int:
    """
    Run pytest with the specified options.
    
    Args:
        test_type: "all", "smoke", "statistics", "users", "posts"
        headless: Whether to run browser in headless mode
        verbose: Whether to run with verbose output
        generate_report: Whether to generate a Markdown report
        base_url: Base URL for the application under test
    
    Returns:
        Exit code from pytest
    """
    test_dir = get_test_dir()
    reports_dir = test_dir / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add test directory
    cmd.append(str(test_dir / "tests"))
    
    # Add marker filter if specified
    if test_type != "all":
        cmd.extend(["-m", test_type])
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    
    # Add short tracebacks
    cmd.append("--tb=short")
    
    # Timestamp for reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate HTML report
    html_report = reports_dir / f"test_results_e2e_{timestamp}.html"
    cmd.extend(["--html", str(html_report), "--self-contained-html"])
    
    # Add custom options
    if headless:
        cmd.append("--headless")
    
    cmd.extend(["--base-url", base_url])
    
    # Print header
    print("=" * 70)
    print(f"  Flask Blog Admin UI - Selenium E2E Test Suite")
    print("=" * 70)
    print(f"  Test Type: {test_type.upper()}")
    print(f"  Browser Mode: {'HEADLESS' if headless else 'VISIBLE'}")
    print(f"  Base URL: {base_url}")
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
        md_report = reports_dir / f"test_results_e2e_{timestamp}.md"
        generate_markdown_report(
            test_type=test_type,
            headless=headless,
            base_url=base_url,
            stdout=process.stdout,
            stderr=process.stderr,
            exit_code=process.returncode,
            output_file=md_report,
            html_report=html_report
        )
        print()
        print("=" * 70)
        print(f"  REPORTS GENERATED")
        print("=" * 70)
        print(f"  📄 Markdown: {md_report.name}")
        print(f"  🌐 HTML:     {html_report.name}")
        print(f"  📁 Location: {reports_dir}")
        print("=" * 70)
    
    return process.returncode


def generate_markdown_report(
    test_type: str,
    headless: bool,
    base_url: str,
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
            parts = line.split()
            for i, part in enumerate(parts):
                try:
                    if "passed" in part.lower():
                        passed = int(parts[i-1].replace(',', ''))
                    if "failed" in part.lower():
                        failed = int(parts[i-1].replace(',', ''))
                    if "skipped" in part.lower():
                        skipped = int(parts[i-1].replace(',', ''))
                    if "error" in part.lower():
                        errors = int(parts[i-1].replace(',', ''))
                except (ValueError, IndexError):
                    pass
    
    total = passed + failed + skipped + errors
    status = "✅ PASSED" if exit_code == 0 else "❌ FAILED"
    
    # Extract test case details
    test_cases_info = extract_test_cases(stdout)
    
    # Build the Markdown report
    report = f"""# E2E Test Execution Report

## Summary

| Metric | Value |
|--------|-------|
| **Test Type** | {test_type.upper()} |
| **Browser Mode** | {'Headless' if headless else 'Visible'} |
| **Base URL** | {base_url} |
| **Execution Time** | {timestamp} |
| **Overall Status** | {status} |
| **Total Tests** | {total} |
| **Passed** | {passed} |
| **Failed** | {failed} |
| **Skipped** | {skipped} |
| **Errors** | {errors} |

## Test Configuration

- **Test Framework**: pytest + Selenium WebDriver
- **Browser**: Chrome {'(Headless)' if headless else '(Visible)'}
- **HTML Report**: [{html_report.name}]({html_report.name})

## Test Cases

| Test ID | Description | Status |
|---------|-------------|--------|
"""
    
    # Add test case rows
    for tc in test_cases_info:
        report += f"| {tc['id']} | {tc['description']} | {tc['status']} |\n"
    
    report += f"""
## Console Output

```
{stdout}
```

"""
    
    if stderr:
        report += f"""## Errors/Warnings

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

Common failure reasons:
- Application not running (ensure Flask server is at the specified base URL)
- Element not found (UI may have changed, update page object selectors)
- Timeout waiting for element (increase implicit wait or add explicit waits)
- Database state (tests may depend on specific data existing)

"""
    
    report += f"""## Test Coverage

These E2E tests cover the following user stories from `user_stories.md`:

### E2E-01: Admin UI loads and shows live statistics
- **TC-E2E-01**: UI loads and displays statistics (smoke test)
- **TC-E2E-02**: Stats refresh updates displayed values

### E2E-02: Admin can create user then create post via UI
- **TC-E2E-03**: Create user → create draft post flow
- **TC-E2E-04**: Create published post variant

---

*Report generated on {timestamp}*
"""
    
    # Write the report
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)


def extract_test_cases(stdout: str) -> list:
    """Extract test case information from pytest output."""
    test_cases = [
        {
            "id": "TC-E2E-01",
            "description": "UI loads and shows stats (smoke)",
            "status": "❓"
        },
        {
            "id": "TC-E2E-02", 
            "description": "Stats refresh updates values",
            "status": "❓"
        },
        {
            "id": "TC-E2E-03",
            "description": "Create user + draft post flow",
            "status": "❓"
        },
        {
            "id": "TC-E2E-04",
            "description": "Create published post",
            "status": "❓"
        }
    ]
    
    # Map test function names to test case IDs
    test_mapping = {
        "test_ui_loads_and_shows_stats": "TC-E2E-01",
        "test_refresh_updates_stats": "TC-E2E-02",
        "test_create_user_and_draft_post": "TC-E2E-03",
        "test_create_published_post": "TC-E2E-04"
    }
    
    # Parse stdout to find test results
    for line in stdout.split("\n"):
        for func_name, tc_id in test_mapping.items():
            if func_name in line:
                if "PASSED" in line:
                    for tc in test_cases:
                        if tc["id"] == tc_id:
                            tc["status"] = "✅ PASSED"
                elif "FAILED" in line:
                    for tc in test_cases:
                        if tc["id"] == tc_id:
                            tc["status"] = "❌ FAILED"
                elif "SKIPPED" in line:
                    for tc in test_cases:
                        if tc["id"] == tc_id:
                            tc["status"] = "⏭️ SKIPPED"
                elif "ERROR" in line:
                    for tc in test_cases:
                        if tc["id"] == tc_id:
                            tc["status"] = "⚠️ ERROR"
    
    return test_cases


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(
        description="Run Selenium E2E tests for Flask Blog Admin UI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_tests.py                      # Run all tests (visible browser)
    python run_tests.py --headless           # Run in headless mode
    python run_tests.py --smoke              # Run smoke tests only
    python run_tests.py --statistics         # Run statistics tests only
    python run_tests.py -v --no-report       # Verbose output, no report
    python run_tests.py --base-url http://localhost:8080  # Custom URL
        """
    )
    
    # Test type selection
    test_group = parser.add_mutually_exclusive_group()
    test_group.add_argument(
        "--smoke", "-s",
        action="store_true",
        help="Run only smoke tests"
    )
    test_group.add_argument(
        "--statistics",
        action="store_true",
        help="Run only statistics tab tests"
    )
    test_group.add_argument(
        "--users",
        action="store_true",
        help="Run only user-related tests"
    )
    test_group.add_argument(
        "--posts",
        action="store_true",
        help="Run only post-related tests"
    )
    
    # Browser options
    parser.add_argument(
        "--headless", "-H",
        action="store_true",
        default=False,
        help="Run tests in headless mode (no visible browser)"
    )
    
    # Output options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=True,
        help="Run with verbose output (default: True)"
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip Markdown report generation"
    )
    
    # Configuration
    parser.add_argument(
        "--base-url",
        default="http://localhost:5000",
        help="Base URL for the application (default: http://localhost:5000)"
    )
    
    args = parser.parse_args()
    
    # Determine test type
    if args.smoke:
        test_type = "smoke"
    elif args.statistics:
        test_type = "statistics"
    elif args.users:
        test_type = "users"
    elif args.posts:
        test_type = "posts"
    else:
        test_type = "all"
    
    # Run the tests
    exit_code = run_pytest(
        test_type=test_type,
        headless=args.headless,
        verbose=args.verbose,
        generate_report=not args.no_report,
        base_url=args.base_url
    )
    
    # Exit with the same code as pytest
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
