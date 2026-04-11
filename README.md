# Placement Portal Application
MAD2 Project

Placement Portal Application (PPA-V2) — Flask & Vue.js Web Application

A full-stack web application built using Flask, Vue.js, SQLite, Celery, and Redis that manages placement operations such as drive management, job applications, interview scheduling, automated reminders, and report generation.

This system provides three separate user roles — Admin, Company, and Student — each with dedicated dashboards and functionality.

## Project Description

The Placement Portal Application is a role-based web application designed for managing college placements efficiently. It provides a clean and effective interface for three types of users:

### Admin
The Admin manages the overall placement system.
They can:
- View all placement drives
- View all applications from students
- Receive monthly placement reports
- View placement statistics

### Company
The Company posts and manages placement drives.
They can:
- Post new placement drives (jobs)
- View applications from students
- Schedule interviews
- Export application data as CSV

### Student
The Student interacts with the placement system.
They can:
- Search and view available jobs
- Apply to placement drives
- View application status
- Track interview schedules
- Export personal application history

## Key Features

- Role-Based Access System (Admin, Company, Student)
- Secure Authentication using JWT tokens
- Job Application Tracking System
- Interview Scheduling and Management
- Automated Email Reminders (via Celery)
- Monthly Report Generation
- Redis Caching for improved performance
- CSV Export functionality
- Responsive Vue.js Frontend
- RESTful Flask API Backend

## Tech Stack

- Flask (Backend API)
- Vue.js (Frontend)
- SQLite (Database)
- Redis (Caching & Message Broker)
- Celery (Async Jobs)
- JWT (Authentication)
- MailHog (Local Email Testing)

## Project Structure (Short Overview)

```
Placement Portal Application/
│
├── backend/                    # Flask Backend
│   ├── app.py                  # Flask Application
│   ├── run.py                  # Database Initialization & Server Startup
│   ├── celery_app.py           # Celery Configuration
│   ├── tasks.py                # Celery Tasks
│   ├── mail.py                 # Email Module
│   ├── requirements.txt        # Python Dependencies
│   ├── models/                 # Database Models
│   ├── routes/                 # API Routes
│   ├── instance/               # SQLite Database
│   └── venv/                   # Virtual Environment
│
├── frontend/                   # Vue.js Frontend
│   ├── src/                    # Source Code
│   ├── package.json            # npm Dependencies
│   ├── vite.config.js          # Vite Configuration
│   └── index.html              # HTML Entry Point
│
└── README.md                   # Project Documentation
```

## Installation Instructions

### Step 1 — Clone the Repository
```bash
git clone <repository-url>
cd "Placement Portal Application"
```

### Step 2 — Backend Setup

#### Create Virtual Environment
```bash
cd backend
python3 -m venv venv
```

#### Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Initialize Database
```bash
python run.py
```

This will:
- Create the SQLite database
- Initialize default branches (CSE, ECE, EEE, MECH, CIVIL, AIML, IT, Bio Tech)
- Create admin user with credentials:
  - **Email:** admin@example.com
  - **Password:** admin123

### Step 4 — Frontend Setup
```bash
cd frontend
npm install
```

## How to Run the Application

You will need to open **7 separate terminal windows** and run these commands in order:

### Terminal 1 — Start Redis Server
```bash
redis-server
```

### Terminal 2 — Start Redis CLI Monitor (Optional)
```bash
redis-cli monitor
```

### Terminal 3 — Start MailHog (SMTP Server)
```bash
mailhog
```
Access email inbox at: http://localhost:8025

### Terminal 4 — Start Flask Backend
```bash
cd backend
source venv/bin/activate
python run.py
```

Backend runs on: http://127.0.0.1:5001

### Terminal 5 — Start Celery Worker
```bash
cd backend
source venv/bin/activate
celery -A celery_app.celery worker --loglevel=info
```

### Terminal 6 — Start Celery Beat Scheduler
```bash
cd backend
source venv/bin/activate
celery -A celery_app.celery beat --loglevel=info
```

### Terminal 7 — Start Frontend Development Server
```bash
cd frontend
npm run dev
```

Frontend runs on: http://localhost:5173

## Manual Task Triggering (Optional Testing)

To trigger Celery tasks immediately, open a new terminal and run:

```bash
cd backend
source venv/bin/activate
python -c "from tasks import generate_monthly_report, send_daily_reminders; generate_monthly_report.delay(); send_daily_reminders.delay()"
```

Then visit http://localhost:8025 to view generated emails in MailHog.

## Default Admin Credentials

- **Email:** admin@example.com
- **Password:** admin123

## Celery Tasks

### send_daily_reminders()
- **Schedule:** Daily at 9:00 AM (IST)
- **Function:** Sends email reminders to students about closing job deadlines and upcoming interviews

### generate_monthly_report()
- **Schedule:** 1st of month at 10:00 AM (IST)
- **Function:** Sends monthly placement statistics report to admin
