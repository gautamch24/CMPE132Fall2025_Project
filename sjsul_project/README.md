# SJSU Library (SJSUL) - Information Security Project

**CMPE 132 – Information Security, Fall 2025**  
**Project Implementation Version 1**

---

## Project Overview

The **SJSU Library (SJSUL)** system is a comprehensive web application demonstrating the four critical phases of identity and access management:

1. **Provisioning** - Creating and configuring user accounts with role assignments
2. **Authentication** - Verifying user identity through secure login with bcrypt password hashing
3. **Authorization** - Controlling access to resources using Role-Based Access Control (RBAC)
4. **De-provisioning** - Disabling user accounts while preserving data integrity

This project implements enterprise-grade security features including password hashing with automatic salt generation, role-based permissions, and comprehensive audit logging.

---

## Tech Stack

| Component | Technology | Version |
|-----------|------------|----------|
| **Language** | Python | 3.11+ |
| **Web Framework** | Flask | 3.0.3 |
| **Authentication** | Flask-Login | 0.6.3 |
| **Forms & CSRF** | Flask-WTF | 1.2.1 |
| **Database ORM** | SQLAlchemy | 2.0.25 |
| **Password Hashing** | Passlib (bcrypt) | 1.7.4 |
| **Database** | SQLite | 3.x |
| **Frontend** | Bootstrap 5 | 5.3.2 |
| **Icons** | Bootstrap Icons | 1.11.1 |
| **Templates** | Jinja2 | (included with Flask) |

---

## Project Structure

```
sjsul_project/
│
├── app.py                 # Main Flask application entry point
├── models.py              # SQLAlchemy ORM models (User, Role, Permission, AuditLog)
├── auth.py                # Authentication routes (login, register, logout)
├── admin.py               # Admin routes (user management, audit logs)
├── security.py            # Security utilities (hashing, authorization decorator)
├── db_seed.py             # Database initialization and seeding script
├── requirements.txt       # Python dependencies
├── README.md              # This file
│
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Base template with navigation
│   ├── login.html         # Login page
│   ├── register.html      # User registration (provisioning)
│   ├── dashboard.html     # User dashboard with roles/permissions
│   ├── users.html         # Admin user management page
│   ├── forbidden.html     # Access denied page (authorization failure)
│   └── approvals.html     # Audit logs viewer
│
├── static/                # Static assets
│   ├── styles.css         # Custom CSS styling
│   └── scripts.js         # Client-side JavaScript
│
└── sjsul.db               # SQLite database (created after seeding)
```

---

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone or Navigate to Project
```bash
cd sjsul_project
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Initialize Database
```bash
python db_seed.py
```

This will:
- Create the SQLite database (`sjsul.db`)
- Create all tables (users, roles, permissions, user_roles, role_permissions, audit_logs)
- Seed demo data (3 roles, 6 permissions, 5 users)
- Display password hashing demonstration

### Step 6: Run the Application
```bash
flask run
```

Or:
```bash
python app.py
```

### Step 7: Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## Demo Credentials

### Admin Account (Full Access)
- **Username:** `admin`
- **Password:** `Password123!`
- **Permissions:** All resources (books, users, reports, audit logs)

### Librarian Account (Moderate Access)
- **Username:** `librarian`
- **Password:** `LibPass456`
- **Permissions:** Manage books, view reports

### Student Account (Limited Access)
- **Username:** `student1`
- **Password:** `Password123!`
- **Permissions:** View books only

### Disabled Account (De-provisioning Demo)
- **Username:** `disabled_user`
- **Password:** `Disabled123`
- **Status:** Account is disabled (cannot login)

---

## Security Features Demonstrated

### 1. Provisioning (User Creation)
- Navigate to `/register` to create new users
- Assign roles during account creation
- Passwords are immediately hashed using bcrypt
- Only password hash is stored (never plaintext)
- Automatic audit log entry created

### 2. Authentication (Login)
- Navigate to `/login`
- Username/password verification using bcrypt
- Failed login attempts are logged
- Disabled accounts cannot authenticate
- Session management via Flask-Login

### 3. Authorization (RBAC)
- **Role-Based Access Control** implemented
- Three roles: Admin, Librarian, Student
- Six permissions: books:read, books:write, books:delete, users:manage, reports:read, audit:read
- `@requires(resource, action)` decorator enforces permissions
- Try accessing `/reports` as a student to see access denial

### 4. De-provisioning (Account Disabling)
- Admin users can navigate to `/admin/users`
- Toggle user accounts between active/disabled
- Disabled users cannot login
- Data is preserved (reversible action)
- All actions are audit logged

### 5. Password Hashing Demonstration
When you run `db_seed.py`, you'll see:
```
Password Hashing Demonstration:
--------------------------------------------------
Both admin and student1 use password: Password123!

admin hash:    $2b$12$...[unique hash]...
student1 hash: $2b$12$...[different hash]...

Note: Same password produces different hashes (bcrypt auto-salting)
```

This demonstrates that identical passwords produce different hashes due to automatic salt generation.

### 6. Audit Logging
- All security events are logged to `audit_logs` table
- Logged events: login attempts, registration, access attempts, user provisioning/de-provisioning
- Admin users can view logs at `/admin/audit-logs`
- Each log includes: user, action, resource, result, timestamp

---

## Required Screenshots

### Screenshot Checklist

Please capture the following screenshots for your submission:

1. **Provisioning (User Registration)**
   - Screenshot of `/register` page
   - Screenshot after successfully creating a new user

2. **De-provisioning (User Disabling)**
   - Screenshot of `/admin/users` page showing active users
   - Screenshot after disabling a user
   - Screenshot of failed login attempt by disabled user

3. **Authentication**
   - Screenshot of successful login
   - Screenshot of failed login (wrong password)

4. **Authorization Success**
   - Screenshot of `/books` page (accessible to all roles)
   - Screenshot of `/reports` page (admin/librarian only)

5. **Authorization Denied**
   - Screenshot of `/forbidden` page when student tries to access `/reports`

6. **Password Hashing Demonstration**
   - Screenshot of terminal output from `python db_seed.py` showing different hashes for same password

7. **Database View**
   - Screenshot of `users` table in SQLite
   - Screenshot of `roles` and `permissions` tables
   - Screenshot of `audit_logs` table

### How to View Database

**Option 1: Using SQLite Browser**
```bash
# Install DB Browser for SQLite (https://sqlitebrowser.org/)
# Open sjsul.db in the browser
```

**Option 2: Using Command Line**
```bash
sqlite3 sjsul.db
.tables
SELECT * FROM users;
SELECT * FROM roles;
SELECT * FROM permissions;
SELECT * FROM audit_logs;
.quit
```

---

## Testing the Four Phases

### Test Provisioning
1. Go to `http://127.0.0.1:5000/register`
2. Create a new user with username `testuser`, email `test@sjsu.edu`, password `Test123!`, role `Student`
3. Verify success message
4. Check audit logs to see the registration event

### Test Authentication
1. Go to `http://127.0.0.1:5000/login`
2. Try logging in with wrong password → Should fail
3. Try logging in with `disabled_user` → Should be denied
4. Login with `admin` / `Password123!` → Should succeed

### Test Authorization
1. Login as `student1` / `Password123!`
2. Access `/books` → Should succeed (student has books:read)
3. Try to access `/reports` → Should be denied (student lacks reports:read)
4. Logout and login as `admin`
5. Access `/reports` → Should succeed (admin has all permissions)

### Test De-provisioning
1. Login as `admin` / `Password123!`
2. Go to `/admin/users`
3. Disable `student2` account
4. Logout
5. Try to login as `student2` → Should be denied with "account disabled" message
6. Login as admin again and re-enable `student2`

---

## Database Schema

### Tables

**users**
- `id` (INTEGER, PRIMARY KEY)
- `username` (VARCHAR, UNIQUE)
- `email` (VARCHAR, UNIQUE)
- `password_hash` (VARCHAR) - bcrypt hash
- `active` (BOOLEAN) - for de-provisioning
- `created_at` (DATETIME)

**roles**
- `id` (INTEGER, PRIMARY KEY)
- `name` (VARCHAR, UNIQUE)
- `description` (VARCHAR)

**permissions**
- `id` (INTEGER, PRIMARY KEY)
- `resource` (VARCHAR) - e.g., 'books', 'users'
- `action` (VARCHAR) - e.g., 'read', 'write', 'manage'

**user_roles** (many-to-many)
- `user_id` (FOREIGN KEY → users.id)
- `role_id` (FOREIGN KEY → roles.id)

**role_permissions** (many-to-many)
- `role_id` (FOREIGN KEY → roles.id)
- `permission_id` (FOREIGN KEY → permissions.id)

**audit_logs**
- `id` (INTEGER, PRIMARY KEY)
- `user_id` (FOREIGN KEY → users.id, NULLABLE)
- `action` (VARCHAR) - e.g., 'login', 'register', 'access'
- `resource` (VARCHAR) - what was accessed
- `result` (VARCHAR) - 'success' or 'failure'
- `timestamp` (DATETIME)

---

## Troubleshooting

### Issue: Module not found
**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Database not found
**Solution:** Run the seeding script:
```bash
python db_seed.py
```

### Issue: Port 5000 already in use
**Solution:** Use a different port:
```bash
flask run --port 5001
```

### Issue: Permission denied on login
**Solution:** Check that the user account is active in the database or via `/admin/users`

---

## Additional Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **Flask-Login:** https://flask-login.readthedocs.io/
- **SQLAlchemy:** https://www.sqlalchemy.org/
- **Passlib (bcrypt):** https://passlib.readthedocs.io/
- **Bootstrap 5:** https://getbootstrap.com/

---

## Reflection Document

See `Reflection.md` in the parent directory for a detailed reflection on the project, including:
- Most intellectually compelling aspects
- Real-world applications
- Implementation challenges
- Security design decisions
- Future improvements

---

## Author

**Course:** CMPE 132 – Information Security  
**Semester:** Fall 2025  
**Institution:** San José State University  
**Project:** SJSU Library (SJSUL) - Security Implementation Ver 1

---

## License

This project is created for educational purposes as part of CMPE 132 coursework.

---

## Project Completion Checklist

- [x] Provisioning implementation (user registration with role assignment)
- [x] Authentication implementation (bcrypt password hashing and verification)
- [x] Authorization implementation (RBAC with @requires decorator)
- [x] De-provisioning implementation (user disable/enable functionality)
- [x] Password hashing demonstration (same password → different hashes)
- [x] Audit logging (all security events tracked)
- [x] Database schema with all required tables
- [x] Bootstrap 5 UI with responsive design
- [x] CSRF protection via Flask-WTF
- [x] Session management via Flask-Login
- [x] Demo credentials and seeded data
- [x] Comprehensive README documentation
- [x] Reflection document (250+ words)
- [ ] Screenshots captured and included
- [ ] Code tested and verified working

---

**Thank you for reviewing the SJSU Library Security Project!**