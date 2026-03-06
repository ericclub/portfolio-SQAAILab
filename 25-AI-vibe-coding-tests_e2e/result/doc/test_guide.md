# E2E Selenium Test Guide

## Overview

This test suite provides end-to-end (E2E) automated tests for the Flask Blog Admin UI using Selenium WebDriver with Python. The tests follow the **Page Object Model** pattern for maintainability and use **pytest** as the test framework.

## Test Cases

| Test ID | Story | Description |
|---------|-------|-------------|
| TC-E2E-01 | E2E-01 | UI loads and displays statistics (smoke test) |
| TC-E2E-02 | E2E-01 | Stats refresh updates displayed values |
| TC-E2E-03 | E2E-02 | Create user → create draft post flow |
| TC-E2E-04 | E2E-02 | Create published post variant |

These tests cover the critical E2E user stories from `20-AI-QA-analysis-assistant/result/doc/user_stories.md`.

---

## Prerequisites

### 1. Software Requirements

- **Python 3.8+** installed
- **Google Chrome** browser installed (latest version recommended)
- **Flask Blog API** application running at `http://localhost:5000`

### 2. Application Setup

Before running tests, ensure the Flask Blog API is running:

```bash
# Navigate to the application directory
cd 10-AI-vibe-coding\result\src\app\backend

# Activate virtual environment (if using)
..\..\.venv\Scripts\activate

# Run the application
python app.py
```

The application should be accessible at `http://localhost:5000`.

---

## Installation

### 1. Navigate to the test directory

```bash
cd 25-AI-vibe-coding-tests_e2e\result\selenium
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `selenium` - Browser automation
- `pytest` - Test framework
- `pytest-html` - HTML report generation
- `webdriver-manager` - Automatic ChromeDriver management

---

## Running Tests

### Basic Usage

```bash
# Run all tests with visible browser (default)
python run_tests.py

# Run all tests in headless mode (no browser window)
python run_tests.py --headless
```

### Test Filtering

```bash
# Run only smoke tests
python run_tests.py --smoke

# Run only statistics tab tests
python run_tests.py --statistics

# Run only user-related tests
python run_tests.py --users

# Run only post-related tests
python run_tests.py --posts
```

### Additional Options

```bash
# Run with verbose output
python run_tests.py --verbose

# Skip Markdown report generation
python run_tests.py --no-report

# Use a different base URL
python run_tests.py --base-url http://localhost:8080

# Combine options
python run_tests.py --headless --smoke --verbose
```

### Using pytest directly

```bash
# Run all tests
pytest tests/ -v

# Run with headless mode
pytest tests/ -v --headless

# Run specific test file
pytest tests/test_statistics.py -v

# Run by marker
pytest tests/ -v -m smoke

# Run specific test
pytest tests/test_statistics.py::TestStatisticsDisplay::test_ui_loads_and_shows_stats -v
```

---

## Test Reports

### Report Location

All reports are saved to the `reports/` directory:

```
selenium/
└── reports/
    ├── test_results_e2e_20260305_160000.html    # HTML report
    ├── test_results_e2e_20260305_160000.md      # Markdown report
    └── screenshots/                              # Screenshots on failure
        └── test_name_timestamp.png
```

### Report Naming Convention

- Format: `test_results_e2e_{YYYYMMDD}_{HHMMSS}.{ext}`
- Example: `test_results_e2e_20260305_160000.html`

### HTML Report

The HTML report provides:
- Summary statistics (passed/failed/skipped)
- Test duration
- Detailed results for each test
- Error messages and stack traces

Open in a web browser for best viewing experience.

### Markdown Report

The Markdown report includes:
- Summary table with key metrics
- Test case status table
- Full console output
- Failed test analysis (if applicable)
- Test coverage information

---

## Project Structure

```
selenium/
├── conftest.py           # Pytest fixtures (driver, base_url, test data)
├── pytest.ini            # Pytest configuration and markers
├── requirements.txt      # Python dependencies
├── run_tests.py          # CLI test runner with report generation
├── test_guide.md         # This documentation
├── pages/                # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py      # Base class with common methods
│   ├── statistics_page.py # Statistics tab interactions
│   ├── users_page.py     # Users tab interactions
│   └── posts_page.py     # Posts tab interactions
├── tests/                # Test modules
│   ├── __init__.py
│   ├── test_statistics.py    # TC-E2E-01, TC-E2E-02
│   └── test_user_post_flow.py # TC-E2E-03, TC-E2E-04
└── reports/              # Generated reports (created on run)
    ├── *.html
    ├── *.md
    └── screenshots/
```

---

## Configuration

### Browser Options

The tests use Chrome browser by default. Options include:

| Option | Description | Default |
|--------|-------------|---------|
| `--headless` | Run without visible browser window | `False` |
| `--window-size` | Browser window dimensions | `1920x1080` |
| Implicit wait | Default wait time for elements | `10s` |

### Base URL

Default: `http://localhost:5000`

Override with: `--base-url http://your-server:port`

### Pytest Markers

Available markers for test filtering:

| Marker | Description |
|--------|-------------|
| `smoke` | Smoke tests for basic functionality |
| `e2e` | End-to-end browser tests |
| `statistics` | Statistics tab tests |
| `users` | User management tests |
| `posts` | Post management tests |

---

## Troubleshooting

### Common Issues

#### 1. "Connection refused" error

**Problem**: Tests fail with connection refused to localhost:5000

**Solution**: Ensure the Flask Blog API is running:
```bash
cd 10-AI-vibe-coding\result\src\app\backend
python app.py
```

#### 2. ChromeDriver version mismatch

**Problem**: "This version of ChromeDriver only supports Chrome version XX"

**Solution**: The `webdriver-manager` package automatically handles this. If issues persist:
```bash
pip install --upgrade webdriver-manager
```

#### 3. Elements not found

**Problem**: Tests fail with "element not found" or timeout errors

**Possible causes**:
- Page not fully loaded (increase wait times)
- UI structure changed (update page object selectors)
- Application error preventing page render

**Solution**: Check the application is working correctly in a manual browser session.

#### 4. Tests pass locally but fail in CI

**Problem**: Tests work on local machine but fail in CI/CD

**Solution**: Ensure CI environment has:
- Chrome browser installed
- `--headless` flag used
- Sufficient wait times for slower environments
- Application running and accessible

### Screenshot on Failure

When a test fails, a screenshot is automatically captured and saved to:
```
reports/screenshots/test_name_timestamp.png
```

---

## Best Practices

### For Developers

1. **Keep tests independent**: Each test should be able to run in isolation
2. **Use unique test data**: Generate unique usernames/emails per test run
3. **Clean up test data**: Consider cleanup strategies for database state
4. **Update page objects**: When UI changes, update selectors in page classes
5. **Run headless in CI**: Use `--headless` for automated pipelines

### For QA Engineers

1. **Run smoke tests first**: Use `--smoke` for quick validation
2. **Check reports**: Review HTML/Markdown reports after each run
3. **Verify prerequisites**: Ensure app is running before test execution
4. **Use visible mode for debugging**: Omit `--headless` to watch test execution

---

## User Story Coverage

### E2E-01: Admin UI loads and shows live statistics

**Acceptance Criteria**:
- UI loads and renders stats from the API ✅
- Refresh updates the displayed stats ✅

**Tests**:
- `test_ui_loads_and_shows_stats` (TC-E2E-01)
- `test_refresh_updates_stats` (TC-E2E-02)

### E2E-02: Admin can create user then create post via UI

**Acceptance Criteria**:
- Create a user via UI and see it listed ✅
- Create a post for the new user via UI and see it listed ✅
- Draft badge displayed for draft posts ✅
- Published badge displayed for published posts ✅

**Tests**:
- `test_create_user_and_draft_post` (TC-E2E-03)
- `test_create_published_post` (TC-E2E-04)

---

## Quick Reference

```bash
# Quick start (after installation)
python run_tests.py

# Headless mode for CI/CD
python run_tests.py --headless

# Smoke tests only
python run_tests.py --smoke --headless

# View results
# Open reports/test_results_e2e_*.html in browser
```

---

*Last updated: March 2026*
