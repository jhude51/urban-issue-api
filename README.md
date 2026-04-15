# Urban Issue Reporting API

A production-oriented backend API for reporting and managing urban infrastructure issues.  
Built with Django REST Framework, PostgreSQL, and environment-based configuration.

---

## Overview

This project is designed to simulate a real-world backend system that allows users to:

- Report urban issues (e.g. potholes, broken infrastructure)
- Retrieve reported issues via API
- Validate incoming data properly
- Persist data in a production-grade database (PostgreSQL)

---

## Tech Stack

- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL  
- **Configuration Management:** python-decouple  
- **Language:** Python  

---

## Features Implemented

- REST API (GET, POST)
- Data validation using serializers
- PostgreSQL integration (production-like setup)
- Environment variable-based configuration
- Django ORM for database interaction
- Admin interface for data management

---

## Project Structure
```
urban-issue-api/
|
├── app/
│ ├── core/
│ ├── issues/
│ └── manage.py
│
├── .env
├── requirements.txt
├── README.md
```
---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/urban-issue-api.git
cd urban-issue-api
```
---

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```
---

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
---

### 4. Setup PostgreSQL
```sql
CREATE DATABASE urban_issue_db;
CREATE USER dayo WITH PASSWORD 'yourpassword';
ALTER ROLE dayo SET client_encoding TO 'utf8';
ALTER ROLE dayo SET default_transaction_isolation TO 'read committed';
ALTER ROLE dayo SET timezone TO 'UTC';
ALTER DATABASE urban_issue_db OWNER TO dayo;
```
Grant required permissions:
```sql
GRANT ALL PRIVILEGES ON DATABASE urban_issue_db TO dayo;
```
---

### 5. Configure environment variables
```.env
DB_NAME=urban_issue_db
DB_USER=dayo
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```
---

### 6. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
---

### 7. Apply migrations
```bash
python manage.py runserver
```
---

## API Endpoints

### GET all issues
```
GET /issues/
``` 
### POST create issue
```
POST /issues/
```
### Sample request:
```json
{
  "title": "Broken traffic light",
  "description": "Not working",
  "location": "Abuja"
}
```
### Validation Example:
```json
{
  "title": ["Title must be at least 5 characters long."]
}
``` 
---

## Key Engineering Concepts Applied

### 1. Serializer-based Validation
Validation is handled at the serializer level, ensuring:
- Clean separation of concerns
- Reusable validation logic
- Structured error responses

---

### 2. ORM vs Raw SQL
Django ORM is used for:
- Rapid development
- Maintainability
- Database abstraction

Raw SQL may still be required for performance-critical operations.

---

### 3. Database Migrations
- `makemigrations` → generates schema change plan  
- `migrate` → applies schema to database  

Migrations act as version control for database structure.

---

### 4. Environment Configuration
Sensitive values are stored outside code using environment variables.

> **Key Insight:** Configuration errors can be more dangerous than code errors.

---

### 5. Debugging Approach
Issues encountered:
- PostgreSQL permission errors (schema access)
- Environment variables not loading correctly

Resolution involved:
- Reading error logs
- Identifying root cause (misconfiguration)
- Applying least-privilege fixes

---

## 🔐 Security Considerations

- No credentials stored in source code  
- `.env` is excluded via `.gitignore`  
- Environment-based configuration enforced  

---

## 🧪 Testing the API

Use:
- Browser (GET requests)
- Postman or curl (POST requests)

---

## 🚧 Next Steps (DevOps Focus)

- Dockerize the application  
- Add CI/CD pipeline  
- Deploy to Azure  
- Introduce Terraform (Infrastructure as Code)  
- Add monitoring (Prometheus + Grafana)  

---

## 📈 Key Takeaways

- Real-world issues are often configuration-related, not code-related  
- Reading error logs is a critical engineering skill  
- Validation should be handled at the correct layer (serializer vs view)  
- Environment variables must be explicitly loaded and managed  

---

## 👤 Author

Built as part of a hands-on DevOps transition journey.