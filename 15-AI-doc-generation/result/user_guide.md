
# Flask Blog API – Technical User Guide 

## Table of Contents
1. Introduction
2. System Overview
3. Architecture
4. Getting Started
5. User Interface Overview
   - Statistics Tab
   - Users Tab
   - Posts Tab
6. Backend API Overview
7. CRUD Workflows
   - User Management
   - Post Management
8. Error Handling & Validation
9. Data Model Overview
10. Security Considerations
11. Good to Know / Best Practices

---

## 1. Introduction
This document is a **User Guide** for the *Flask Blog API Admin Interface*.  
It is intended for **Clients, Product Owners, QA Analysts, and other stakeholders** who want to understand how the software works functionally.

The application provides:
- A RESTful backend API (Flask + SQLAlchemy)
- A lightweight admin web interface (HTML + JavaScript)
- Full CRUD operations for Users and Blog Posts
- Global statistics dashboard

---

## 2. System Overview
The system is composed of two main parts:

- **Backend**: Flask REST API connected to a MySQL database
- **Frontend**: Single-page admin interface communicating via HTTP (JSON)

Typical use cases:
- Create and manage users
- Create, publish, and delete blog posts
- View global platform statistics

---

## 3. Architecture

**Frontend (Browser)**
- HTML + JavaScript
- Uses `fetch()` to call REST endpoints
- Runs independently from backend

**Backend (Flask API)**
- Flask + SQLAlchemy ORM
- MySQL database
- CORS enabled for frontend access

**Database**
- Users table
- Posts table (linked to users)

---

## 4. Getting Started

### Prerequisites
- Python 3.9+
- MySQL database
- Browser (Chrome, Edge, Firefox)

### Backend Startup
1. Configure database connection (environment variable or default)
2. Run:
```bash
python app.py
```
3. Database tables are auto-created on startup

### Frontend Startup
- Open `index.html` in a browser
- Backend must be running at `http://localhost:5000`

---

## 5. User Interface Overview

### 📊 Statistics Tab
Displays real-time platform metrics:
- Total Users
- Total Posts
- Published Posts

**Actions**
- Refresh statistics manually

**Purpose**
- High-level monitoring for stakeholders

---

### 👥 Users Tab
Allows full user management.

**Features**
- Create user (username, email, password)
- View all users
- Delete users

**Notes**
- Username and email must be unique
- Deleting a user also deletes their posts

---

### 📝 Posts Tab
Manages blog posts.

**Features**
- Create posts
- Assign author (User ID)
- Draft or Published status
- View post list
- Delete posts

**Notes**
- A user must exist before creating a post
- Only published posts count as public content

---

## 6. Backend API Overview

### Health Check
`GET /api/health`

### Users
- `POST /api/users`
- `GET /api/users`
- `GET /api/users/{id}`
- `DELETE /api/users/{id}`

### Posts
- `POST /api/posts`
- `GET /api/posts`
- `GET /api/posts/{id}`
- `PUT /api/posts/{id}`
- `DELETE /api/posts/{id}`

### Statistics
- `GET /api/stats`

---

## 7. CRUD Workflows

### User – CRUD Example

**Create**
```json
POST /api/users
{
  "username": "john",
  "email": "john@email.com",
  "password": "secret"
}
```

**Read**
```http
GET /api/users
```

**Delete**
```http
DELETE /api/users/1
```

---

### Post – CRUD Example

**Create**
```json
POST /api/posts
{
  "title": "My First Post",
  "content": "Hello world",
  "user_id": 1,
  "published": true
}
```

**Read**
```http
GET /api/posts
```

**Update**
```json
PUT /api/posts/1
{
  "published": false
}
```

**Delete**
```http
DELETE /api/posts/1
```

---

## 8. Error Handling & Validation
- Missing fields → HTTP 400
- Duplicate username/email → HTTP 409
- Resource not found → HTTP 404
- Server error → HTTP 500

All errors return JSON responses.

---

## 9. Data Model Overview

### User
- id
- username (unique)
- email (unique)
- password_hash
- created_at

### Post
- id
- title
- content
- published
- created_at
- updated_at
- user_id (foreign key)

---

## 10. Security Considerations
- Passwords are hashed (Werkzeug)
- No authentication layer (admin-only prototype)
- CORS enabled (development mode)
- Not production-ready without auth & HTTPS

---

## 11. Good to Know / Best Practices
- Always create users before posts
- Use Statistics tab for smoke testing
- Ideal project for:
  - QA automation practice
  - API testing
  - CRUD validation scenarios
- Can be extended with:
  - Authentication (JWT)
  - Role-based access
  - Pagination & search

---

**End of User Guide**
