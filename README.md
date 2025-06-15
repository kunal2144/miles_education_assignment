# 📝 Miles Education Assignment – User Activity Logs API

This Django project implements a simple API for logging user activities such as logins, tracking metadata, and updating the status of those logs. The API also uses caching to improve the performance of log retrievals using Redis.

---

## 🔧 Prerequisites

Make sure the following services are installed and running:
- ✅ **PostgreSQL** (e.g., `sudo apt install postgresql`)
- ✅ **Redis Server** (e.g., `sudo apt install redis-server`)

---

## 🗄️ PostgreSQL Setup

### 1. Create a new PostgreSQL user and database

Log in to PostgreSQL as the `postgres` superuser:
```bash
sudo -u postgres psql
```

Then run the following SQL:
```sql
CREATE USER activity_user WITH PASSWORD 'yourpassword';
CREATE DATABASE activity_db OWNER activity_user;
-- Grant schema privileges
GRANT CONNECT ON DATABASE activity_db TO activity_user;
\c activity_db
GRANT USAGE, CREATE ON SCHEMA public TO activity_user;
ALTER SCHEMA public OWNER TO activity_user;
```

Exit psql:
```sql
\q
```

---

## 🚀 Project Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/kunal2144/miles_education_assignment.git
cd miles_education_assignment
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Ensure your `.env` contains correct database and Redis info.

### 5. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Server
```bash
python manage.py runserver
```

---

## 📬 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/token/` | Login and get token |
| POST | `/api/logs/` | Create a new log entry |
| GET | `/api/logs/` | List all user logs |
| PATCH | `/api/logs/<id>/` | Update a log's status |

🔐 **All endpoints except `/api/token/` require authentication.**

---

## 🧪 Testing the API with Postman

This project includes a ready-to-use Postman collection:

1. Open Postman.
2. Click **File** → **Import** → select `postman_collection.json`.
3. Send the **Get Token** request — the script will automatically save the token to the collection variables.
4. Use the other requests: Create, List, Update logs.