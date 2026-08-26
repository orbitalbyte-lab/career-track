# CareerTrack

A professional job and internship application tracking system built with Python.

CareerTrack helps students, internship seekers, recent graduates, and early-career professionals organize and track their job applications in one place.


## Screenshots

Coming soon.

Future versions will include screenshots of:

- Company management
- Application management
- Dashboard analytics
- CSV import and export

## Features

### Company Management

* Add companies
* View companies
* Update companies
* Delete companies
* Search companies

### Application Management

* Add applications
* View applications
* Update applications
* Delete applications
* Search applications
* Filter applications
* Sort applications

### Dashboard and Analytics

* Total applications
* Applications by status
* Applications by company
* Applications by application type
* Monthly application statistics
* Location statistics
* Upcoming deadlines
* Success rate

### CSV Support

* Export applications to CSV
* Import applications from CSV

### Testing

* 109 automated tests


## Technology Stack

| Technology  | Purpose                   |
| ----------- | ------------------------- |
| Python 3.13 | Core programming language |
| SQLite      | Database                  |
| SQLAlchemy  | ORM                       |
| Pytest      | Automated testing         |
| Git         | Version control           |
| GitHub      | Source code hosting       |



## Project Structure

career-track/
├── app/
│   ├── cli/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   └── main.py
├── docs/
├── exports/
├── tests/
└── README.md


## Installation

Clone the repository:

git clone <repository-url>

Move into the project directory:

cd career-track

Create a virtual environment:

python -m venv .venv

Activate the virtual environment:

**Windows PowerShell**

.venv\Scripts\Activate.ps1

Install the project:

pip install -e .


## Running the Application

Start the application:

python -m app.main

The CLI menu includes:

- Company management
- Application management
- Dashboard analytics
- CSV import
- CSV export
- Application sorting

## Running the Tests

Run all tests:

pytest

Run a specific test file:

pytest tests/test_main.py -v


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


## Application Statuses

* Wishlist
* Applied
* Under Review
* Interview
* Offer
* Rejected
* Withdrawn


## Future Improvements

* Interview management
* Follow-up reminders
* User authentication
* Email notifications
* Resume management
* AI-powered job matching
* AI resume analysis
* Web interface
* Cloud deployment


## Software Engineering Practices

This project follows modern software engineering practices:

- Layered architecture
- Repository pattern
- Service layer
- Separation of concerns
- Automated testing
- Git version control
- Incremental feature development
- Documentation-driven development

Development statistics:

- 109 automated tests
- Multiple feature branches and commits
- SQLite database integration
- CSV import and export support



## License

This project was developed for educational and portfolio purposes.
