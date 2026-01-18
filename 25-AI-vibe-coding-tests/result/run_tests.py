"""
Test Runner Script for Flask Blog API Tests
Generates Markdown test results report.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --unit       # Run only unit tests
    python run_tests.py --integration # Run only integration tests
"""

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path


def get_timestamp():
    """Get current timestamp for report filename."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def run_tests(test_type=None):
    """
    Run pytest with specified test type and generate Markdown report.
    
    Args:
        test_type: 'unit', 'integration', or None for all tests
    """
    # Change to the result directory
    result_dir = Path(__file__).parent
    os.chdir(result_dir)
    
    # Build pytest command
    cmd = [sys.executable, '-m', 'pytest', '-v', '--tb=short']
    
    # Add marker filter based on test type
    if test_type == 'unit':
        cmd.extend(['-m', 'unit', 'test/unit/'])
        report_name = f"test_results_unit_{get_timestamp()}.md"
    elif test_type == 'integration':
        cmd.extend(['-m', 'integration', 'test/integration/'])
        report_name = f"test_results_integration_{get_timestamp()}.md"
    else:
        report_name = f"test_results_all_{get_timestamp()}.md"
    
    # Create reports directory if not exists
    reports_dir = result_dir / 'reports'
    reports_dir.mkdir(exist_ok=True)
    report_path = reports_dir / report_name
    
    print("=" * 60)
    print(f"🧪 Running {'all' if test_type is None else test_type} tests...")
    print("=" * 60)
    print()
    
    # Run pytest and capture output
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=result_dir
    )
    
    # Print output to console
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    # Generate Markdown report
    generate_markdown_report(
        report_path,
        result.stdout,
        result.stderr,
        result.returncode,
        test_type
    )
    
    print()
    print("=" * 60)
    print(f"📄 Report saved to: {report_path}")
    print("=" * 60)
    
    return result.returncode


def generate_markdown_report(report_path, stdout, stderr, return_code, test_type):
    """Generate a Markdown formatted test report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_type_label = test_type.capitalize() if test_type else "All"
    status = "✅ PASSED" if return_code == 0 else "❌ FAILED"
    
    # Parse test results from stdout
    lines = stdout.split('\n')
    
    # Find summary line
    summary_line = ""
    for line in lines:
        if 'passed' in line or 'failed' in line or 'error' in line:
            if '==' in line:
                summary_line = line.strip('= ')
                break
    
    # Extract test results
    test_results = []
    for line in lines:
        if '::' in line and ('PASSED' in line or 'FAILED' in line or 'ERROR' in line):
            test_results.append(line.strip())
    
    # Generate report content
    report_content = f"""# Test Results Report

## Summary

| Property | Value |
|----------|-------|
| **Date/Time** | {timestamp} |
| **Test Type** | {test_type_label} Tests |
| **Status** | {status} |
| **Summary** | {summary_line} |

---

## Test Results

| Test | Status |
|------|--------|
"""
    
    for test in test_results:
        if 'PASSED' in test:
            status_icon = "✅ PASSED"
        elif 'FAILED' in test:
            status_icon = "❌ FAILED"
        else:
            status_icon = "⚠️ ERROR"
        
        # Clean up test name
        test_name = test.split(' ')[0].replace('::', ' → ')
        report_content += f"| `{test_name}` | {status_icon} |\n"
    
    report_content += f"""
---

## Full Output

```
{stdout}
```
"""
    
    if stderr:
        report_content += f"""
## Errors/Warnings

```
{stderr}
```
"""
    
    report_content += f"""
---

*Report generated automatically by run_tests.py*
"""
    
    # Write report
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--unit', '-u']:
            return run_tests('unit')
        elif arg in ['--integration', '-i']:
            return run_tests('integration')
        elif arg in ['--help', '-h']:
            print(__doc__)
            return 0
    
    return run_tests()


if __name__ == '__main__':
    sys.exit(main())
