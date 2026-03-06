# Flask Blog API Test Guide

This guide explains how to run the unit and integration tests for the Flask Blog API application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Running Tests](#running-tests)
5. [Test Categories](#test-categories)
6. [Test Reports](#test-reports)
7. [Test Cases Coverage](#test-cases-coverage)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Project Structure

```
25-AI-vibe-coding-tests/
└── result/
    └── test/
        ├── conftest.py           # Shared pytest fixtures
        ├── pytest.ini            # Pytest configuration
        ├── requirements.txt      # Test dependencies
        ├── run_tests.py          # Test runner script
        ├── unit/                 # Unit tests
        │   ├── __init__.py
        │   ├── test_user_validation.py
        │   ├── test_post_validation.py
        │   └── test_response_shapes.py
        ├── integration/          # Integration tests
        │   ├── __init__.py
        │   ├── test_health.py
        │   ├── test_users.py
        │   ├── test_posts.py
        │   ├── test_stats.py
        │   ├── test_cors.py
        │   └── test_error_handling.py
        └── reports/              # Generated test reports
```

## Installation

1. **Navigate to the test directory:**

   ```bash
   cd 25-AI-vibe-coding-tests/result/test
   ```

2. **Create and activate a virtual environment (recommended):**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

### Using the Test Runner Script

The `run_tests.py` script provides a convenient way to run tests with various options:

```bash
# Run ALL tests (unit + integration)
python run_tests.py

# Run only UNIT tests
python run_tests.py --unit
# or
python run_tests.py -u

# Run only INTEGRATION tests
python run_tests.py --integration
# or
python run_tests.py -i

# Run with verbose output
python run_tests.py --verbose
# or
python run_tests.py -v

# Run without generating Markdown report
python run_tests.py --no-report
```

### Using pytest Directly

You can also use pytest directly for more control:

```bash
# Run all tests
pytest unit integration -v

# Run only unit tests
pytest unit -v -m unit

# Run only integration tests
pytest integration -v -m integration

# Run tests for a specific feature (using markers)
pytest -m users -v        # User-related tests
pytest -m posts -v        # Post-related tests
pytest -m stats -v        # Statistics tests
pytest -m health -v       # Health check tests

# Run a specific test file
pytest integration/test_users.py -v

# Run a specific test class
pytest integration/test_users.py::TestCreateUser -v

# Run a specific test method
pytest integration/test_users.py::TestCreateUser::test_create_user_with_valid_data -v
```

## Test Categories

### Unit Tests (`unit/`)

Unit tests validate business logic without HTTP calls or database access:

| Test File | Description |
|-----------|-------------|
| `test_user_validation.py` | User model serialization, password handling, validation logic |
| `test_post_validation.py` | Post model serialization, default values, validation logic |
| `test_response_shapes.py` | API response structure validation |

### Integration Tests (`integration/`)

Integration tests validate API endpoints with Flask test client and in-memory SQLite database:

| Test File | Description |
|-----------|-------------|
| `test_health.py` | Health endpoint (HLTH-01) |
| `test_users.py` | User CRUD operations (USR-01 to USR-04) |
| `test_posts.py` | Post CRUD operations (PST-01 to PST-06) |
| `test_stats.py` | Statistics endpoint (STS-01) |
| `test_cors.py` | CORS configuration (NFR-02) |
| `test_error_handling.py` | Error handling and JSON responses (NFR-01, NFR-03) |

### Test Markers

Tests are tagged with markers for selective execution:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.health` - Health check tests
- `@pytest.mark.users` - User management tests
- `@pytest.mark.posts` - Post management tests
- `@pytest.mark.stats` - Statistics tests

## Test Reports

Test reports are automatically generated in the `reports/` directory:

### Report Locations

```
reports/
├── test_results_all_YYYYMMDD_HHMMSS.md      # All tests report
├── test_results_all_YYYYMMDD_HHMMSS.html    # HTML report
├── test_results_unit_YYYYMMDD_HHMMSS.md     # Unit tests report
├── test_results_unit_YYYYMMDD_HHMMSS.html   # HTML report
├── test_results_integration_YYYYMMDD_HHMMSS.md   # Integration tests report
└── test_results_integration_YYYYMMDD_HHMMSS.html # HTML report
```

### Markdown Report Contents

Each Markdown report includes:

- **Summary**: Test type, timestamp, overall status, total/passed/failed counts
- **Test Configuration**: Framework and HTML report reference
- **Console Output**: Full pytest output with test results
- **Failed Tests Analysis**: Details on any failures (if applicable)

### Viewing Reports

- **Markdown**: Open `.md` files in any text editor or Markdown viewer
- **HTML**: Open `.html` files in a web browser for interactive viewing

## Test Cases Coverage

### User Stories Coverage

| Story ID | Description | Test Type | Test File |
|----------|-------------|-----------|-----------|
| HLTH-01 | Health check | Integration | `test_health.py` |
| USR-01 | Create user | Both | `test_users.py`, `test_user_validation.py` |
| USR-02 | List users | Integration | `test_users.py` |
| USR-03 | View user by ID | Integration | `test_users.py` |
| USR-04 | Delete user (cascade) | Integration | `test_users.py` |
| PST-01 | Create post | Both | `test_posts.py`, `test_post_validation.py` |
| PST-02 | List all posts | Integration | `test_posts.py` |
| PST-03 | List published posts | Integration | `test_posts.py` |
| PST-04 | View post by ID | Integration | `test_posts.py` |
| PST-05 | Update post | Integration | `test_posts.py` |
| PST-06 | Delete post | Integration | `test_posts.py` |
| STS-01 | View statistics | Integration | `test_stats.py` |
| NFR-01 | JSON responses | Integration | `test_error_handling.py` |
| NFR-02 | CORS enabled | Integration | `test_cors.py` |

### Test Cases Matrix

| Test Case ID | Description | Test Method |
|--------------|-------------|-------------|
| TC-HLTH-01 | Health check returns OK | `test_health_check_returns_200` |
| TC-USR-01 | Create user with valid data | `test_create_user_with_valid_data` |
| TC-USR-02 | Reject missing fields | `test_create_user_missing_*` |
| TC-USR-03 | Reject duplicate username | `test_create_user_duplicate_username` |
| TC-USR-04 | Reject duplicate email | `test_create_user_duplicate_email` |
| TC-USR-05 | List users returns array | `test_list_users_returns_array` |
| TC-USR-06 | List users empty | `test_list_users_empty_database` |
| TC-USR-07 | Get user by valid ID | `test_get_user_by_valid_id` |
| TC-USR-08 | Get user not found | `test_get_user_not_found` |
| TC-USR-09 | Delete user success | `test_delete_user_success` |
| TC-USR-10 | Delete user cascades posts | `test_delete_user_cascade_posts` |
| TC-USR-11 | Delete user not found | `test_delete_user_not_found` |
| TC-PST-01 | Create post valid data | `test_create_post_with_valid_data` |
| TC-PST-02 | Create post missing fields | `test_create_post_missing_*` |
| TC-PST-03 | Create post user not found | `test_create_post_user_not_found` |
| TC-PST-04 | List posts ordered | `test_list_posts_ordered_by_created_at_desc` |
| TC-PST-05 | List posts empty | `test_list_posts_empty_database` |
| TC-PST-06 | List published only | `test_list_published_posts_only` |
| TC-PST-07 | List published empty | `test_list_published_posts_empty` |
| TC-PST-08 | Get post by valid ID | `test_get_post_by_valid_id` |
| TC-PST-09 | Get post not found | `test_get_post_not_found` |
| TC-PST-10 | Update post publish | `test_update_post_publish` |
| TC-PST-11 | Update post fields | `test_update_post_title_and_content` |
| TC-PST-12 | Update post not found | `test_update_post_not_found` |
| TC-PST-13 | Delete post success | `test_delete_post_success` |
| TC-PST-14 | Delete post not found | `test_delete_post_not_found` |
| TC-STS-01 | Stats returns zeros | `test_stats_empty_database` |
| TC-STS-02 | Stats reflect data | `test_stats_reflect_created_data` |
| TC-STS-03 | Stats cascade impact | `test_stats_cascade_impact` |

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'app'**
   
   Ensure you're running tests from the correct directory and the source path is configured in `conftest.py`.

2. **Database connection errors**
   
   Tests use SQLite in-memory database. No MySQL connection is required for testing.

3. **Import errors for Flask dependencies**
   
   Install all requirements: `pip install -r requirements.txt`

4. **pytest not found**
   
   Ensure pytest is installed: `pip install pytest`

### Getting Help

- Review the test configuration in `pytest.ini`
- Check the fixtures in `conftest.py`
- Examine individual test files for specific test implementations

---

*Last updated: March 2026*
