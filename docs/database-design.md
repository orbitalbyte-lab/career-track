# CareerTrack — Database Design

## Entities

CareerTrack will initially contain five primary entities:

1. User
2. Company
3. Application
4. Interview
5. FollowUp

## User

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | String | User's name |
| email | String | User's email |
| password_hash | String | Secure password hash |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## Company

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | String | Company name |
| website | String | Company website |
| industry | String | Industry |
| location | String | Company location |
| notes | Text | Additional information |
| created_at | DateTime | Creation timestamp |

## Application

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User |
| company_id | Integer | Foreign key to Company |
| position | String | Job or internship position |
| application_type | String | Job or internship |
| date_applied | Date | Application date |
| deadline | Date | Application deadline |
| status | String | Current application status |
| location | String | Job location |
| job_url | String | Original job posting |
| notes | Text | Additional notes |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## Interview

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| application_id | Integer | Foreign key to Application |
| scheduled_at | DateTime | Interview date and time |
| interview_type | String | Type of interview |
| status | String | Interview status |
| notes | Text | Interview notes |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## FollowUp

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| application_id | Integer | Foreign key to Application |
| follow_up_date | Date | Follow-up date |
| notes | Text | Follow-up notes |
| completed | Boolean | Whether follow-up is complete |
| created_at | DateTime | Creation timestamp |

## Relationships

- One User can have many Applications.
- One Company can have many Applications.
- One Application belongs to one User.
- One Application belongs to one Company.
- One Application can have many Interviews.
- One Application can have many FollowUps.