## Simple Web Blog - Test Automation

### AI-Assisted

This section of the project focuses on applying AI techniques to **QA Test Planning and Selenium Test Automation**.

### Objectives

As a QA Analyst and Test Developer  
I need automated end-to-end tests for the Simple Web Blog application  
So I will be able to ensure the quality and reliability of the Users, Posts, and Statistics features

1. Create a comprehensive test plan with User Stories, acceptance criteria, and test cases
2. Implement automated Selenium/Python tests based on the test plan
3. Generate test reports in Markdown format

### Tools & Technologies

1. **AI Models:** Claude Opus 4.5 (GitHub Copilot)
2. **Frameworks:** Selenium WebDriver 4.x, Pytest, webdriver-manager
3. **Backend:** Flask REST API (Python)
4. **Frontend:** HTML/CSS/JavaScript
5. **Browsers:** Chrome (default), Edge, Firefox

### How proceeded

1. **Prompt using RCTEFT format:** Provided role (QA Analyst), context (source code), task (test plan + Selenium tests), expected output (Markdown, test files), format (French documentation), and tone (professional)

2. **Test Plan Creation:** AI analyzed the source code (`app.py`, `index.html`, `app.js`) and generated a structured test plan with 13 User Stories and 39 test cases across 3 test suites

3. **Selenium Environment Setup:** AI installed required packages (selenium, webdriver-manager, pytest, pytest-html) and created configuration files

4. **Test Implementation:** AI created comprehensive test files following the naming convention `FEATURE_PRIORITY_ID` with fixtures for browser management and cleanup

5. **Test Runner Creation:** AI built a CLI-based test runner with filtering by feature, priority, and test ID, plus Markdown report generation

ℹ️ See [chat_history.md](chat_history.md) for details 

### Results

* [test_plan.md](test_plan.md) - Comprehensive test plan in French (13 User Stories, 39 Test Cases)
* [INSTALL_Selenium.md](INSTALL_Selenium.md) - Selenium installation report
* [selenium_test_suite_usage.md](selenium_test_suite_usage.md) - Test suite usage documentation
* `../src/test_selenium/` - Complete Selenium test suite:
  * `conftest.py` - Pytest fixtures and browser configuration
  * `base_test.py` - Base test class with reusable utilities
  * `test_users.py` - 12 tests for Users section
  * `test_posts.py` - 15 tests for Posts section
  * `test_statistics.py` - 12 tests for Statistics section
  * `run_tests.py` - Main test runner with CLI interface

### My AI Discoveries 

Using AI assistance for test automation provided significant value:

- **Rapid Analysis:** AI quickly analyzed the entire codebase and identified all testable features and edge cases
- **Consistency:** The generated test plan follows a uniform structure with proper traceability between User Stories and Test Cases
- **Best Practices:** AI implemented Selenium best practices (Page Object patterns, explicit waits, proper cleanup)
- **Documentation:** Comprehensive documentation was generated alongside the code, reducing manual effort
- **Custom Requirements:** AI adapted to specific requirements (French documentation, custom naming conventions, flexible test runner)
- **Time Savings:** What would typically take several days of manual work was completed in a single session
- **Interactive Problem-Solving:** AI provided real-time assistance during troubleshooting, analyzing error messages, suggesting solutions, and guiding through each fix step-by-step. This interactive debugging capability significantly accelerated issue resolution compared to traditional documentation searches
- **Contextual Understanding:** AI maintained awareness of the entire project context, allowing it to provide targeted solutions that considered the specific environment (Windows, Python 3.14, VS Code) and project structure

### Challenges

Several technical challenges were encountered and successfully resolved during the implementation:

1. **Flask Import Resolution**
   - **Problem:** Python interpreter couldn't resolve Flask imports in the backend code
   - **Solution:** Created a virtual environment (`.venv`) and installed Flask with `py -m pip install flask`, then selected the correct Python interpreter in VS Code

2. **Python Interpreter Selection**
   - **Problem:** Uncertainty about which Python interpreter to use for the project
   - **Solution:** Created a dedicated virtual environment in the project directory and selected `.venv/Scripts/python.exe` as the interpreter

3. **Test Execution Freeze**
   - **Problem:** Tests appeared to freeze indefinitely when running `python run_tests.py --test-id TC-001-01`
   - **Root Cause:** Backend Flask server (port 5000) and frontend server (port 8080) were not running
   - **Solution:** Started both servers in separate terminals before launching tests

4. **ChromeDriver SSL Download Error**
   - **Problem:** `webdriver-manager` failed to download ChromeDriver due to SSL certificate errors (`SSLEOFError`)
   - **Solution:** Downloaded ChromeDriver v145.0.7632.110 manually from Chrome for Testing and configured `conftest.py` to use the local path (`C:\chromedriver\chromedriver.exe`)

5. **Unicode Encoding in Windows Console**
   - **Problem:** Tests failed with `UnicodeEncodeError` when printing special characters (➤, émojis) to the Windows console using cp1252 encoding
   - **Solution:** Added UTF-8 encoding configuration at the start of `conftest.py`:
     ```python
     if sys.platform == 'win32':
         sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
         sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
     ```
   - **Impact:** This global fix enabled all tests to use special characters without modification

6. **Server Coordination**
   - **Problem:** Tests require both backend (Flask) and frontend (static server) to be running simultaneously
   - **Solution:** Established a clear startup procedure: Terminal 1 for backend (port 5000), Terminal 2 for frontend (port 8080), Terminal 3 for tests, with verification steps for each service



   All this done in 5 hours !  ![alt text](image.png)