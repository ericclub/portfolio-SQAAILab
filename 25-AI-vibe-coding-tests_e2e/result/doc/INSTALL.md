# Simple Web Blog - Installation Guide

A complete web blog application with Python Flask backend and HTML/JavaScript frontend.

## Prerequisites

Before installing, ensure you have the following installed on your PC:

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **MySQL Server 8.0+** (optional) - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
3. **VS Code** (optional but recommended) - [Download VS Code](https://code.visualstudio.com/)

> **Note:** By default, the application uses SQLite (no additional database installation required). MySQL is optional and can be enabled via environment variables.

## Project Structure

```
DEMO-Vibe-Coding/result/src/app/
├── backend/
│   ├── app.py              # Flask REST API server
│   └── requirements.txt    # Python dependencies
└── frontend/
    ├── index.html          # Main HTML page
    ├── css/
    │   └── style.css       # Stylesheet
    └── js/
        └── app.js          # JavaScript application
```

## Installation Steps

### Step 1: Configure Backend Environment

1. Open a terminal in VS Code (`` Ctrl+` ``)
2. Navigate to the backend folder:

```powershell
cd "DEMO-Vibe-Coding/result/src/app/backend"
```

3. Create a virtual environment (recommended):

```powershell
python -m venv venv
```

4. Activate the virtual environment:

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Or Windows Command Prompt
.\venv\Scripts\activate.bat
```

5. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

### Step 2: Database Configuration (Optional)

**By default, the application uses SQLite** which requires no additional setup. The database file `blog.db` is created automatically in the backend folder.

**To use MySQL instead:**

1. First, create the MySQL database:

```sql
CREATE DATABASE blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Set environment variables before running the application:

```powershell
# Windows PowerShell
$env:USE_SQLITE = "false"
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = "your_password"
$env:DB_NAME = "blog_db"
```

### Step 3: Run the Backend Server

From the backend directory, run:

```powershell
python app.py
```

You should see:
```
Database tables created successfully!
Starting Blog API Server...
API available at: http://localhost:5000/api
Health check: http://localhost:5000/api/health
```

### Step 4: Run the Frontend

**Option A: Using VS Code Live Server extension (recommended)**

1. Install the "Live Server" extension in VS Code
2. Right-click on `frontend/index.html`
3. Select "Open with Live Server"
4. The browser will open automatically

**Option B: Using Python's built-in HTTP server**

Open a new terminal and run:

```powershell
cd "DEMO-Vibe-Coding/result/src/app/frontend"
python -m http.server 8080
```

Then open `http://localhost:8080` in your browser.

**Option C: Open directly in browser**

Simply double-click `frontend/index.html` to open it in your default browser.

> **Note:** Some browsers may block API calls when opening files directly. Use Option A or B if you encounter issues.

## API Endpoints

The backend provides the following REST API endpoints:

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | List all users |
| GET | `/api/users/{id}` | Get user details |
| POST | `/api/users` | Create a new user |
| DELETE | `/api/users/{id}` | Delete a user |

### Posts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts` | List all posts |
| GET | `/api/posts/{id}` | Get post details |
| POST | `/api/posts` | Create a new post |
| PUT | `/api/posts/{id}` | Update a post |
| DELETE | `/api/posts/{id}` | Delete a post |

### Statistics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Get general statistics |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Check server status |

## Usage Guide

### Creating Users

1. Click "Users" in the navigation
2. Click "+ New User"
3. Enter username and email
4. Click "Create User"

### Creating Posts

1. Click "Posts" in the navigation
2. Click "+ New Post"
3. Enter title, content, and select an author
4. Click "Save Post"

### Viewing Statistics

1. Click "Statistics" in the navigation
2. View total users, posts, and activity data
3. Click "Refresh" to update statistics

## Troubleshooting

### Common Issues

**1. "Cannot connect to MySQL"**
- Verify MySQL service is running
- Check database credentials in `app.py`
- Ensure the database `blog_db` exists

**2. "CORS error in browser console"**
- Make sure the backend server is running on port 5000
- The Flask-CORS extension should handle CORS automatically

**3. "Module not found" errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**4. "Port 5000 already in use"**
- Another application is using port 5000
- Change the port in `app.py`: `app.run(port=5001)`
- Update `API_BASE_URL` in `frontend/js/app.js`

### MySQL Service Commands (Windows)

```powershell
# Check MySQL service status
Get-Service MySQL*

# Start MySQL service
Start-Service MySQL80

# Stop MySQL service
Stop-Service MySQL80
```

## Technology Stack

- **Backend**: Python 3.8+, Flask, Flask-SQLAlchemy, Flask-CORS, PyMySQL
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: MySQL 8.0+
- **API**: RESTful design

## Features Implemented

- [x] Create a user
- [x] List all users
- [x] View user details
- [x] Delete a user
- [x] Create a post
- [x] List all posts
- [x] View post details
- [x] Edit a post
- [x] Delete a post
- [x] View general statistics

## License

Demo application for educational purposes.
