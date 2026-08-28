# CareerTrack

A professional job and internship application tracking system built with Python.

CareerTrack helps students, internship seekers, recent graduates, and early-career professionals organize, track, and analyze their job applications, interviews, and follow-ups in one place.

---

## Screenshots

Coming soon.

Future versions will include screenshots of:

* Company management
* Application management
* Interview management
* Follow-up management
* Dashboard analytics
* CSV import and export

---

## Features

### Company Management

* Add companies
* View companies
* Update companies
* Delete companies
* Search companies
* Store company website, industry, location, and notes

### Application Management

* Add applications
* View applications
* Update applications
* Delete applications
* Search applications
* Filter applications
* Sort applications
* Track application status
* Track application type
* Track application deadlines
* Store job URLs and notes
* Filter applications by company, status, type, and date

### Interview Management

* Create interviews
* View interviews
* Delete interviews
* Search interviews
* Sort interviews by scheduled date
* Sort interviews by interview type
* Track interview status
* Track interview type
* Track scheduled interview dates

### Follow-up Management

* Create follow-up reminders
* View follow-ups
* Complete follow-ups
* Reopen completed follow-ups
* Delete follow-ups
* View pending follow-ups
* View completed follow-ups
* View upcoming follow-ups
* Track follow-up statistics

### Dashboard and Analytics

* Total applications
* Applications by status
* Applications by application type
* Applications by company
* Monthly application statistics
* Location statistics
* Upcoming application deadlines
* Success rate
* Application filtering and sorting

### CSV Support

* Export applications to CSV
* Import applications from CSV
* Export interview data to CSV

### Logging

CareerTrack includes application logging for monitoring important application events and errors.

* File-based logging
* Console logging
* Timestamped log messages
* INFO-level application events
* Dedicated application log directory

### Testing

The project includes a comprehensive automated test suite covering:

* Domain models
* Database integration
* Repositories
* Services
* CLI functionality
* CSV import/export
* Interview management
* Follow-up management
* Application management
* Company management
* Dashboard statistics
* Resource cleanup

**109 automated tests currently pass successfully.**

Tests are also verified with Python `ResourceWarning` treated as an error to help detect resource-management problems.

---

## Technology Stack

| Technology  | Purpose                      |
| ----------- | ---------------------------- |
| Python 3.13 | Core programming language    |
| SQLite      | Database                     |
| SQLAlchemy  | ORM and database interaction |
| Pytest      | Automated testing            |
| Setuptools  | Python package management    |
| Git         | Version control              |
| GitHub      | Source code hosting          |

---

## Architecture

CareerTrack follows a layered architecture designed to keep responsibilities separated.

```text
CLI Layer
   ↓
Service Layer
   ↓
Repository Layer
   ↓
Database Layer
```

### CLI Layer

Handles user interaction and command-line menus.

```text
app/cli/
├── application_menu.py
├── company_menu.py
├── follow_up_menu.py
├── interview_menu.py
└── menu.py
```

### Service Layer

Contains application business logic.

```text
app/services/
├── application_service.py
├── company_service.py
├── export_service.py
├── follow_up_service.py
├── import_service.py
└── interview_service.py
```

### Repository Layer

Handles database operations.

```text
app/repositories/
├── application_repository.py
├── company_repository.py
├── follow_up_repository.py
└── interview_repository.py
```

### Database Layer

Contains SQLAlchemy database configuration and database models.

```text
app/database/
├── connection.py
├── init_db.py
└── models/
    ├── application.py
    ├── company.py
    ├── follow_up.py
    └── interview.py
```

### Domain Models

```text
app/models/
├── application.py
├── company.py
├── follow_up.py
└── interview.py
```

---

## Project Structure

```text
career-track/
├── app/
│   ├── cli/
│   │   ├── application_menu.py
│   │   ├── company_menu.py
│   │   ├── follow_up_menu.py
│   │   ├── interview_menu.py
│   │   └── menu.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── init_db.py
│   │   └── models/
│   │       ├── application.py
│   │       ├── company.py
│   │       ├── follow_up.py
│   │       └── interview.py
│   │
│   ├── models/
│   │   ├── application.py
│   │   ├── company.py
│   │   ├── follow_up.py
│   │   └── interview.py
│   │
│   ├── repositories/
│   │   ├── application_repository.py
│   │   ├── company_repository.py
│   │   ├── follow_up_repository.py
│   │   └── interview_repository.py
│   │
│   ├── services/
│   │   ├── application_service.py
│   │   ├── company_service.py
│   │   ├── export_service.py
│   │   ├── follow_up_service.py
│   │   ├── import_service.py
│   │   └── interview_service.py
│   │
│   ├── logging_config.py
│   └── main.py
│
├── docs/
│   ├── database-design.md
│   └── requirements.md
│
├── tests/
│   ├── conftest.py
│   ├── data/
│   │   └── sample.csv
│   ├── test_application.py
│   ├── test_company.py
│   ├── test_database.py
│   ├── test_export_service.py
│   ├── test_follow_up.py
│   ├── test_follow_up_repository.py
│   ├── test_follow_up_service.py
│   ├── test_import_service.py
│   ├── test_interview_repository.py
│   ├── test_interview_service.py
│   ├── test_main.py
│   ├── test_repositories.py
│   └── test_services.py
│
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/orbitalbyte-lab/career-track.git
```

### 2. Move into the project directory

```bash
cd career-track
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install the project

```bash
pip install -e .
```

---

## Running the Application

Start CareerTrack with:

```bash
python -m app.main
```

The CLI provides functionality for:

* Company management
* Application management
* Interview management
* Follow-up management
* Dashboard analytics
* CSV import
* CSV export
* Application searching
* Application filtering
* Application sorting

---

## Running the Tests

Run the complete test suite:

```bash
python -m pytest -q
```

Run the complete test suite while treating resource warnings as errors:

```bash
python -W error::ResourceWarning -m pytest -q
```

Run a specific test file:

```bash
python -m pytest tests/test_main.py -vv
```

Current test result:

```text
109 passed
```

---

## Database Design

### Company

| Field    | Type    |
| -------- | ------- |
| id       | Integer |
| name     | String  |
| website  | String  |
| industry | String  |
| location | String  |
| notes    | Text    |

### Application

| Field            | Type    |
| ---------------- | ------- |
| id               | Integer |
| company_id       | Integer |
| position         | String  |
| application_type | String  |
| date_applied     | Date    |
| deadline         | Date    |
| status           | String  |
| location         | String  |
| job_url          | String  |
| notes            | Text    |

### Interview

| Field          | Type     |
| -------------- | -------- |
| id             | Integer  |
| application_id | Integer  |
| scheduled_at   | DateTime |
| interview_type | String   |
| status         | String   |

### Follow-up

| Field          | Type     |
| -------------- | -------- |
| id             | Integer  |
| application_id | Integer  |
| follow_up_at   | DateTime |
| note           | Text     |
| completed      | Boolean  |

---

## Application Statuses

CareerTrack supports the following application statuses:

* Wishlist
* Applied
* Under Review
* Interview
* Offer
* Rejected
* Withdrawn

---

## Interview Management

CareerTrack supports multiple interview stages and types, allowing users to track interviews associated with applications.

Interview information includes:

* Scheduled date and time
* Interview type
* Interview status
* Related application

---

## Follow-up Management

Follow-ups help users remember important actions after submitting applications or completing interviews.

Examples include:

* Email recruiter
* Send additional documents
* Follow up after interview
* Check application status
* Contact hiring manager

Follow-ups can be marked as completed and reopened when necessary.

---

## Data Import and Export

CareerTrack supports CSV-based data management.

### Export

Application and interview information can be exported for:

* Backup
* Analysis
* Sharing
* External processing

### Import

Applications can also be imported from CSV files.

---

## Logging

Application logs are stored locally during development.

```text
logs/
└── career_track.log
```

Generated logs and other local development artifacts are excluded from version control through `.gitignore`.

---

## Development Practices

CareerTrack follows modern software engineering practices, including:

* Layered architecture
* Repository pattern
* Service layer
* Separation of concerns
* Domain models
* Database abstraction
* Automated testing
* Test fixtures
* Resource cleanup
* Logging
* Git version control
* Incremental feature development
* Documentation-driven development
* CSV data import/export

---

## Development Statistics

* **109 automated tests**
* **All tests passing**
* **Python 3.13**
* **SQLite database integration**
* **SQLAlchemy ORM**
* **CSV import/export**
* **Interview management**
* **Follow-up management**
* **Application logging**
* **Repository and service architecture**
* **GitHub version control**

---

## Future Improvements

Planned future improvements include:

* User authentication
* User accounts and profiles
* Email notifications
* Resume management
* Resume/CV attachment support
* AI-powered job matching
* AI-powered resume analysis
* Web interface
* REST API
* Cloud database support
* Cloud deployment
* Advanced analytics dashboard
* Automated follow-up notifications
* Calendar integration

---

## License

This project was developed for educational and portfolio purposes.
