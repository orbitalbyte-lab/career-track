[![CI](https://github.com/orbitalbyte-lab/career-track/actions/workflows/ci.yml/badge.svg)](https://github.com/orbitalbyte-lab/career-track/actions/workflows/ci.yml)

# CareerTrack

CareerTrack is a Python-based job and internship application tracking system designed for students, internship seekers, recent graduates, and early-career professionals.

It provides a command-line interface and REST API for managing companies, applications, interviews, and follow-ups, with authentication, user ownership isolation, analytics, CSV import/export, database migrations, automated testing, and continuous integration.

## Highlights

* Company, application, interview, and follow-up management
* REST API built with FastAPI
* JWT-based authentication
* Password hashing with Argon2
* User ownership and resource isolation
* Application filtering, sorting, and analytics
* Interview and follow-up tracking
* CSV import and export
* SQLAlchemy ORM
* Alembic database migrations
* PostgreSQL integration tests
* Automated CI with GitHub Actions
* 430 automated tests
* 97.18% test coverage
* Ruff code-quality checks
* Python 3.13

---

## Features

### Company Management

* Create companies
* View companies
* Update companies
* Delete companies
* Search companies
* Store website, industry, location, and notes
* Restrict company access to the authenticated owner

### Application Management

* Create applications
* View applications
* Update applications
* Delete applications
* Search applications
* Filter applications by:

  * status
  * application type
  * company
  * application date
* Sort applications
* Track deadlines
* Validate application dates and deadlines
* Store job URLs and notes
* Restrict applications to the owning user

### Interview Management

* Create interviews
* View interviews
* Update interview status and outcome
* Delete interviews
* Search interviews
* Sort interviews
* Track interview type
* Track interview status
* Track scheduled date and time
* Require timezone-aware interview timestamps
* Restrict interviews to the owning user

### Follow-up Management

* Create follow-up reminders
* View follow-ups
* Update completion status
* Complete follow-ups
* Reopen follow-ups
* Delete follow-ups
* View pending follow-ups
* View completed follow-ups
* View upcoming follow-ups
* Require timezone-aware follow-up timestamps
* Restrict follow-ups to the owning user

### Dashboard and Analytics

CareerTrack provides application and interview analytics including:

* Total applications
* Applications by status
* Applications by application type
* Applications by company
* Monthly application statistics
* Location statistics
* Upcoming application deadlines
* Application success rate
* Interview statistics
* Filtering and sorting support

### CSV Import and Export

* Export applications to CSV
* Import applications from CSV
* Export interview data to CSV

### Authentication and Security

* User registration
* User login
* JWT access tokens
* Authenticated `/me` endpoint
* Password hashing using Argon2
* Password verification
* Expired-token rejection
* Invalid-signature rejection
* Bearer authentication enforcement
* Inactive-user rejection
* Malformed JWT claim rejection
* User-level ownership isolation

### API Validation

The REST API validates request data at the boundary using Pydantic, including:

* Email format validation
* Password length limits
* String length limits
* Positive resource IDs
* Enum validation
* Date validation
* Timezone-aware datetime validation
* Job URL validation
* Application deadline validation
* Pagination limits

---

## REST API

The API is implemented with FastAPI.

### Authentication

POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me

### Companies

POST   /api/companies
GET    /api/companies
GET    /api/companies/{company_id}
PUT    /api/companies/{company_id}
DELETE /api/companies/{company_id}

### Applications

POST   /api/applications
GET    /api/applications
GET    /api/applications/{application_id}
PUT    /api/applications/{application_id}
DELETE /api/applications/{application_id}

### Interviews

POST   /api/interviews
GET    /api/interviews
GET    /api/interviews/{interview_id}
PUT    /api/interviews/{interview_id}
DELETE /api/interviews/{interview_id}

### Follow-ups

POST   /api/follow-ups
GET    /api/follow-ups
GET    /api/follow-ups/{follow_up_id}
PUT    /api/follow-ups/{follow_up_id}
DELETE /api/follow-ups/{follow_up_id}

### Health and Documentation

GET /health
GET /docs
GET /openapi.json

When the application is running locally, interactive Swagger documentation is available at:

http://127.0.0.1:8000/docs

---

## Authentication Flow

CareerTrack uses JWT-based authentication.

User
  │
  ├── Register
  │      ↓
  │   Password hashed with Argon2
  │      ↓
  │   User stored in database
  │
  └── Login
         ↓
      Credentials verified
         ↓
      JWT access token
         ↓
      Authorization: Bearer <token>
         ↓
      Current authenticated user

Protected resources use the authenticated user's ID to enforce ownership.

A user cannot read, update, delete, or create dependent resources under another user's companies or applications.

---

## Architecture

CareerTrack uses a layered architecture with a separate API layer and CLI layer.

                    ┌─────────────────────┐
                    │      REST API       │
                    │      FastAPI        │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │    Service Layer    │
                    │  Business Logic     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Repository Layer    │
                    │ Database Operations │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Database Layer    │
                    │ SQLAlchemy / DB     │
                    └─────────────────────┘

CLI ───────────────► Service Layer

### API Layer

app/api/
├── dependencies.py
├── main.py
├── routers/
│   ├── auth.py
│   ├── companies.py
│   ├── applications.py
│   ├── interviews.py
│   └── follow_ups.py
└── schemas/
    ├── auth.py
    ├── token.py
    ├── company.py
    ├── application.py
    ├── interview.py
    └── follow_up.py

Responsibilities:

* HTTP routing
* Authentication dependencies
* Request validation
* Response serialization
* HTTP error handling

### Security Layer


app/security/
├── jwt.py
└── passwords.py

Responsibilities:

* JWT creation and validation
* Secure password hashing
* Password verification

### Service Layer


app/services/
├── application_service.py
├── auth_service.py
├── company_service.py
├── export_service.py
├── follow_up_service.py
├── import_service.py
└── interview_service.py

Responsibilities:

* Business rules
* Validation that depends on existing data
* Ownership checks
* Coordination between repositories

### Repository Layer

app/repositories/
├── application_repository.py
├── company_repository.py
├── follow_up_repository.py
├── interview_repository.py
└── user_repository.py

Responsibilities:

* Database queries
* CRUD operations
* Filtering
* Sorting
* Ownership-aware data access

### Database Layer

app/database/
├── connection.py
├── init_db.py
└── models/
    ├── user.py
    ├── company.py
    ├── application.py
    ├── interview.py
    └── follow_up.py

### Domain Models

app/models/
├── application.py
├── company.py
├── follow_up.py
└── interview.py

### CLI Layer

app/cli/
├── application_menu.py
├── company_menu.py
├── follow_up_menu.py
├── interview_menu.py
└── menu.py

---

## Project Structure

career-track/
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   ├── routers/
│   │   └── schemas/
│   │
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
│   │
│   ├── models/
│   ├── repositories/
│   ├── security/
│   ├── services/
│   ├── config.py
│   ├── logging_config.py
│   └── main.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── docs/
│   ├── database-design.md
│   └── requirements.md
│
├── tests/
│   ├── api/
│   ├── integration/
│   ├── security/
│   ├── data/
│   └── unit and service tests
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md

---

## Technology Stack

| Technology      | Purpose                               |
| --------------- | ------------------------------------- |
| Python 3.13     | Application language                  |
| FastAPI         | REST API                              |
| Pydantic        | Request and response validation       |
| SQLAlchemy      | ORM and database access               |
| Alembic         | Database migrations                   |
| PostgreSQL      | Relational database integration       |
| SQLite          | Lightweight local/test database usage |
| PyJWT           | JWT authentication                    |
| pwdlib + Argon2 | Password hashing                      |
| Pytest          | Automated testing                     |
| pytest-cov      | Coverage reporting                    |
| Ruff            | Linting and code quality              |
| Setuptools      | Python packaging                      |
| Git             | Version control                       |
| GitHub Actions  | Continuous integration                |

---

## Database Design

### User

| Field         | Type     | Description             |
| ------------- | -------- | ----------------------- |
| id            | Integer  | Primary key             |
| email         | String   | Unique normalized email |
| password_hash | String   | Secure password hash    |
| is_active     | Boolean  | Account status          |
| created_at    | DateTime | Creation timestamp      |
| updated_at    | DateTime | Last update timestamp   |

### Company

| Field    | Type    | Description      |
| -------- | ------- | ---------------- |
| id       | Integer | Primary key      |
| user_id  | Integer | Owning user      |
| name     | String  | Company name     |
| website  | String  | Company website  |
| industry | String  | Industry         |
| location | String  | Location         |
| notes    | Text    | Additional notes |

### Application

| Field            | Type    | Description                   |
| ---------------- | ------- | ----------------------------- |
| id               | Integer | Primary key                   |
| company_id       | Integer | Related company               |
| position         | String  | Job or internship position    |
| application_type | String  | Internship, scholarship, etc. |
| date_applied     | Date    | Application date              |
| deadline         | Date    | Application deadline          |
| status           | String  | Current application status    |
| location         | String  | Position location             |
| job_url          | String  | Job listing URL               |
| notes            | Text    | Additional notes              |

### Interview

| Field          | Type     | Description              |
| -------------- | -------- | ------------------------ |
| id             | Integer  | Primary key              |
| application_id | Integer  | Related application      |
| scheduled_at   | DateTime | Scheduled interview time |
| interview_type | String   | Interview type           |
| status         | String   | Interview status         |
| outcome        | String   | Interview outcome        |
| notes          | Text     | Additional notes         |

### Follow-up

| Field          | Type     | Description         |
| -------------- | -------- | ------------------- |
| id             | Integer  | Primary key         |
| application_id | Integer  | Related application |
| follow_up_at   | DateTime | Reminder time       |
| note           | Text     | Follow-up note      |
| completed      | Boolean  | Completion status   |

---

## Application Statuses

CareerTrack supports:

Wishlist
Applied
Under Review
Interview
Offer
Rejected
Withdrawn

---

## Database Migrations

Alembic is used for schema migrations.

Create a migration:

python -m alembic revision --autogenerate -m "describe change"

Apply migrations:

python -m alembic upgrade head

Check the current database revision:

python -m alembic current

Verify that the model and migration state are synchronized:

python -m alembic check

---

## Installation

### 1. Clone the repository

git clone https://github.com/orbitalbyte-lab/career-track.git
cd career-track

### 2. Create a virtual environment

python -m venv .venv

### 3. Activate the environment

Windows PowerShell:

.venv\Scripts\Activate.ps1

### 4. Install the project with development dependencies

python -m pip install -e ".[dev]"

The project dependencies are declared in `pyproject.toml`.

---

## Environment Variables

### JWT Secret

Generate a secure local secret:

$env:JWT_SECRET_KEY = (python -c "import secrets; print(secrets.token_hex(32))")

The application requires `JWT_SECRET_KEY` when creating or decoding access tokens.

Never commit a real secret to Git.

### PostgreSQL

The PostgreSQL connection is configured through:

DATABASE_URL

Example:

postgresql+psycopg://postgres:postgres@localhost:5432/career_track

Use environment-specific credentials rather than committing production credentials to the repository.

---

## Running the CLI

Start the command-line application with:

python -m app.main

The CLI provides:

* Company management
* Application management
* Interview management
* Follow-up management
* Dashboard analytics
* Searching
* Filtering
* Sorting
* CSV import
* CSV export

---

## Running the API

Start the FastAPI development server with:

uvicorn app.api.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Swagger UI:

http://127.0.0.1:8000/docs

OpenAPI specification:

http://127.0.0.1:8000/openapi.json

Health endpoint:

http://127.0.0.1:8000/health

---

## Testing

Run the complete test suite:

python -m pytest -v

Run with coverage:

python -m pytest --cov=app --cov-report=term-missing

Run the same coverage gate used by CI:

python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=95

Run a specific test module:

python -m pytest tests/api/test_auth.py -v

Run linting:

ruff check .

Check dependencies:

python -m pip check

---

## Current Test Status

The current project baseline is:

430 tests passed

97.18% total coverage

95% minimum coverage enforced by CI

0 test warnings

The test suite covers:

* API endpoints
* Authentication
* JWT validation
* Password hashing
* User ownership isolation
* Domain models
* Database integration
* PostgreSQL integration
* Repositories
* Services
* CLI functionality
* CSV import/export
* Analytics
* Validation
* Resource cleanup
* Health and OpenAPI endpoints

---

## Continuous Integration

GitHub Actions runs the project checks on pushes and pull requests targeting `master`.

The CI pipeline:

1. Creates a PostgreSQL service
2. Sets up Python 3.13
3. Installs the project and development dependencies
4. Runs Ruff
5. Applies Alembic migrations
6. Runs the full test suite
7. Enforces a minimum 95% coverage threshold

Workflow:

.github/workflows/ci.yml

---

## Logging

CareerTrack includes application logging for important events and errors.

Development logs are stored locally:

logs/
└── career_track.log

Local logs and development artifacts are excluded from version control.

---

## Development Practices

The project follows software engineering practices including:

* Layered architecture
* Separation of concerns
* Repository pattern
* Service layer
* Domain models
* API schemas
* Authentication and authorization
* Automated testing
* High test coverage
* Database migrations
* PostgreSQL integration testing
* Static analysis with Ruff
* CI with GitHub Actions
* Resource cleanup
* Incremental development
* Documentation-driven development
* Git-based version control

---

## Future Improvements

Potential future development areas include:

* Email notifications
* Resume and CV management
* Resume attachment storage
* AI-assisted job matching
* AI-assisted resume analysis
* Web frontend
* Advanced analytics visualization
* Calendar integration
* Automated reminder notifications
* Cloud deployment
* Additional API features
* Role-based administration

---

## Project Status

CareerTrack is an actively developed portfolio project demonstrating practical Python software engineering concepts across:

Python
├── CLI development
├── REST API development
├── Authentication
├── Authorization
├── Database design
├── ORM usage
├── Repository patterns
├── Service-layer architecture
├── Automated testing
├── Security testing
├── Database migrations
├── PostgreSQL integration
├── CI/CD
└── Documentation

---

## License

This project was developed for educational and portfolio purposes.
