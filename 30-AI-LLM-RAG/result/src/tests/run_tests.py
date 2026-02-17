"""Test runner script for LLM RAG automated tests."""
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_tests(test_type: str = "all", report: bool = True):
    """Run tests with optional HTML report generation.
    
    Args:
        test_type: Type of tests to run - 'all', 'infrastructure', 'api', 'performance', 'rag'
        report: Whether to generate HTML report
    """
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Build pytest command using current Python interpreter
    cmd = [sys.executable, "-m", "pytest", "-v"]
    
    # Select test file based on type
    test_files = {
        "all": None,  # Run all
        "infrastructure": "test_infrastructure.py",
        "api": "test_llm_api.py",
        "performance": "test_performance.py",
        "rag": "test_rag_validation.py",
    }
    
    if test_type in test_files and test_files[test_type]:
        cmd.append(test_files[test_type])
    
    # Add report generation
    if report:
        report_file = reports_dir / f"test_results_{test_type}_{timestamp}.html"
        cmd.extend(["--html", str(report_file), "--self-contained-html"])
    
    # Run tests
    print(f"Running {test_type} tests...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    
    if report:
        print("-" * 50)
        print(f"Report saved to: {report_file}")
    
    return result.returncode


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run LLM RAG automated tests")
    parser.add_argument(
        "type",
        nargs="?",
        default="all",
        choices=["all", "infrastructure", "api", "performance", "rag"],
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip HTML report generation"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Skip slow tests (marked with @pytest.mark.slow)"
    )
    
    args = parser.parse_args()
    
    # Modify command for quick mode
    if args.quick:
        import os
        os.environ["PYTEST_ADDOPTS"] = '-m "not slow"'
    
    exit_code = run_tests(args.type, report=not args.no_report)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
