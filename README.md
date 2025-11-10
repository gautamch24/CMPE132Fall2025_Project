### 1. Navigate to project folder
cd sjsul_project
### 2. Activate virtual environment
source venv/bin/activate
### 3. Install dependencies (first time only)
pip install -r requirements.txt
### 4. Initialize database (first time only)
python db_seed.py
### 5. Run the application
flask run
### 6. Open in browser
http://127.0.0.1:5000/
## Demo Accounts
- Admin: admin / Password123!
- Librarian: librarian / LibPass456
- Student:student1 / Password123!
- Disabled:disabled_user / Disabled123
