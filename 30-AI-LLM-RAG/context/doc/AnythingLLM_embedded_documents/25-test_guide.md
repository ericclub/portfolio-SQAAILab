# Test Guide

This document explains how to set up, run, and interpret the automated tests for the Flask Blog API.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running Tests](#running-tests)
5. [Test Structure](#test-structure)
6. [Test Results](#test-results)
7. [Test Coverage](#test-coverage)

---

## Overview

This test suite implements **unit tests** and **integration tests** for the Flask Blog API based on the user stories defined in `user_stories.md`. The tests follow the **Test Pyramid Principle**:

- **Unit tests**: Fast, isolated tests for validation, serialization, and business logic
- **Integration tests**: Full HTTP request/response cycle with database operations

> **Note**: End-to-end (E2E) tests are not included in this suite and will be handled separately.

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

---

## Installation

### 1. Navigate to the test directory

```bash
cd 25-AI-vibe-coding-tests/result
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running Tests

### Run All Tests

```bash
python run_tests.py
```

Or using pytest directly:

```bash
pytest -v
```

### Run Only Unit Tests

```bash
python run_tests.py --unit
```

Or using pytest directly:

```bash
pytest -v -m unit test/unit/
```

### Run Only Integration Tests

```bash
python run_tests.py --integration
```

Or using pytest directly:

```bash
pytest -v -m integration test/integration/
```

### Additional Pytest Options

```bash
# Run with detailed output
pytest -v --tb=long

# Run a specific test file
pytest test/unit/test_users_unit.py -v

# Run a specific test class
pytest test/integration/test_users_integration.py::TestCreateUser -v

# Run a specific test function
pytest test/unit/test_health_unit.py::TestHealthEndpointUnit::test_health_response_contains_status_key -v

# Run with coverage report
pytest --cov=. --cov-report=html
```

---

## Test Structure

```
25-AI-vibe-coding-tests/result/
├── conftest.py              # Pytest fixtures and configuration
├── pytest.ini               # Pytest settings
├── requirements.txt         # Test dependencies
├── run_tests.py             # Test runner with Markdown report generation
├── test_guide.md            # This documentation
├── reports/                 # Generated test reports (Markdown)
└── test/
    ├── __init__.py
    ├── unit/                # Unit tests
    │   ├── __init__.py
    │   ├── test_health_unit.py
    │   ├── test_users_unit.py
    │   ├── test_posts_unit.py
    │   └── test_stats_unit.py
    └── integration/         # Integration tests
        ├── __init__.py
        ├── test_health_integration.py
        ├── test_users_integration.py
        ├── test_posts_integration.py
        ├── test_stats_integration.py
        └── test_nfr_integration.py
```

---

## Test Results

### Console Output

When running tests, results are displayed in the console with:
- ✅ Green checkmarks for passed tests
- ❌ Red X for failed tests
- Summary of passed/failed/skipped tests

### Markdown Reports

Test reports are automatically generated in the `reports/` directory:

| Report File | Description |
|-------------|-------------|
| `test_results_all_YYYYMMDD_HHMMSS.md` | Results from running all tests |
| `test_results_unit_YYYYMMDD_HHMMSS.md` | Results from running unit tests only |
| `test_results_integration_YYYYMMDD_HHMMSS.md` | Results from running integration tests only |

Each report contains:
- Timestamp and test type
- Pass/Fail status summary
- Individual test results table
- Full console output

---

## Test Coverage

### Unit Tests

| Test File | Coverage |
|-----------|----------|
| `test_health_unit.py` | HLTH-01 (response structure) |
| `test_users_unit.py` | USR-01 to USR-04 (validation, serialization, password hashing) |
| `test_posts_unit.py` | PST-01 to PST-03 (validation, serialization, defaults) |
| `test_stats_unit.py` | STS-01 (response structure) |

### Integration Tests

| Test File | Coverage |
|-----------|----------|
| `test_health_integration.py` | HLTH-01 (HTTP contract) |
| `test_users_integration.py` | USR-01 to USR-11 (full CRUD + cascade) |
| `test_posts_integration.py` | PST-01 to PST-14 (full CRUD + filtering) |
| `test_stats_integration.py` | STS-01 to STS-03 (data accuracy) |
| `test_nfr_integration.py` | NFR-01, NFR-02 (JSON responses, CORS, HTTP codes) |

### Test Cases Mapping

| User Story | Unit Tests | Integration Tests |
|------------|------------|-------------------|
| HLTH-01 | ✅ | ✅ |
| USR-01 | ✅ | ✅ |
| USR-02 | ✅ | ✅ |
| USR-03 | - | ✅ |
| USR-04 | - | ✅ |
| PST-01 | ✅ | ✅ |
| PST-02 | ✅ | ✅ |
| PST-03 | ✅ | ✅ |
| PST-04 | - | ✅ |
| PST-05 | - | ✅ |
| PST-06 | - | ✅ |
| STS-01 | ✅ | ✅ |
| NFR-01 | - | ✅ |
| NFR-02 | - | ✅ |

---

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'app'**

Ensure you're running tests from the `result` directory:
```bash
cd 25-AI-vibe-coding-tests/result
pytest -v
```

**2. Database connection errors**

Tests use an in-memory SQLite database, so no external database is required. If you see MySQL errors, ensure the test fixtures are being used correctly.

**3. Import errors**

Verify all dependencies are installed:
```bash
pip install -r requirements.txt
```

---

## Contributing

When adding new tests:

1. Place unit tests in `test/unit/`
2. Place integration tests in `test/integration/`
3. Use appropriate markers (`@pytest.mark.unit` or `@pytest.mark.integration`)
4. Follow the naming convention `test_<feature>_<type>.py`
5. Document test case coverage in this guide

---

*Generated for the SQAAILab Flask Blog API Test Suite*
