# SkillSwap

A university-level peer skill exchange platform where students can offer skills they know and request skills they want to learn. Built with Python and Oracle Database as a Database Systems semester project.

---

## What It Does

Students register, browse skills offered by other students, send session requests, confirm sessions, exchange messages, and leave feedback - all within a structured role-based system. Admins manage users, skills, and skill suggestions from a separate dashboard.

---

## Features

### Student
- Register and log in with bcrypt-hashed passwords
- Post skill offers with proficiency level and session mode (online / in-person / both)
- Set weekly availability slots per offer (day + time slot)
- Browse all available offers from other students
- Send session requests with urgency level and a note
- Select a specific availability slot when requesting
- Accept or reject incoming requests
- Cancel your own pending requests
- Schedule sessions after a request is accepted
- Confirm session completion (auto-completes when both parties confirm)
- In-session messaging between offer and request participants
- Submit feedback after a completed session
- Suggest new skills for admin review
- Receive real-time notifications for matches, sessions, feedback, endorsements, and messages
- Personal dashboard with stats, upcoming session, and recent feedback

### Admin
- View platform-wide stats (users, skills, offers, requests, sessions, pending requests)
- See most requested skill, most offered skill, top rated tutor
- Activate or deactivate user accounts
- Reset any user's password
- Add and delete skills
- Review, approve, or reject student skill suggestions

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| GUI | CustomTkinter |
| Database | Oracle Database |
| DB Driver | python-oracledb |
| Auth | bcrypt |
| Config | python-dotenv |

---

## Database Design

**13 Tables:** `DEPARTMENTS`, `SKILL_CATEGORIES`, `SKILLS`, `USERS`, `SKILL_SUGGESTIONS`, `OFFERS`, `AVAILABILITY`, `REQUESTS`, `SESSIONS`, `FEEDBACK`, `ENDORSEMENTS`, `MESSAGES`, `NOTIFICATIONS`

**13 Triggers:**

| Trigger | Purpose |
|---|---|
| `trg_no_duplicate_requests` | Prevents duplicate active requests for the same skill |
| `trg_no_self_request` | Prevents requesting your own offer |
| `trg_validate_availability` | Ensures selected availability belongs to the chosen offer |
| `trg_auto_complete_session` | Auto-completes session when both parties confirm |
| `trg_no_feedback_before_complete` | Blocks feedback submission until session is completed |
| `trg_no_self_endorsement` | Prevents self-endorsement |
| `trg_prevent_offer_delete` | Blocks deletion of offers with active scheduled sessions |
| `trg_validate_message_session` | Ensures only session participants can send messages |
| `trg_notif_request_accepted` | Notifies requester when their request is accepted |
| `trg_notif_session_created` | Notifies both users when a session is scheduled |
| `trg_notif_feedback_submitted` | Notifies offerer when feedback is received |
| `trg_notif_endorsement_submitted` | Notifies user when they receive an endorsement |
| `trg_notif_message` | Notifies the other participant when a message is sent |

Schema is in **3NF**. All surrogate PKs, proper FK constraints, CHECK constraints, and indexes on frequently queried columns.

---

## Project Structure

```
SkillSwap/
├── main.py                        # Entry point
├── config.example.env             # Environment variable template
│
├── database/
│   ├── SkillSwap.sql              # Full schema: tables, indexes, triggers, seed data
│   └── db_connection.py           # Oracle connection manager
│
├── services/
│   ├── auth_service.py            # Login, registration, password management
│   ├── student_service.py         # All student-facing DB operations
│   └── admin_service.py           # All admin-facing DB operations
│
├── gui/
│   ├── auth/
│   │   ├── login_page.py
│   │   └── register_page.py
│   │
│   ├── admin/
│   │   ├── admin_dashboard.py
│   │   ├── users_page.py
│   │   ├── skills_page.py
│   │   └── suggestions_page.py
│   │
│   ├── student/
│   │   ├── student_dashboard.py
│   │   ├── dashboard_page.py
│   │   ├── offers_page.py
│   │   ├── browse_skills_page.py
│   │   ├── my_requests_page.py
│   │   ├── incoming_requests_page.py
│   │   ├── sessions_page.py
│   │   ├── messages_page.py
│   │   ├── notifications_page.py
│   │   ├── offer_dialog.py
│   │   ├── request_dialog.py
│   │   ├── session_dialog.py
│   │   ├── feedback_dialog.py
│   │   ├── availability_dialog.py
│   │   ├── view_availability_dialog.py
│   │   └── suggest_skill_dialog.py
│   │
│   └── components/
│       └── skill_dialog.py
│
└── utils/
    ├── password_utils.py          # bcrypt hash and verify
    └── table_style.py             # Shared treeview styling
```

---

## Setup

### Prerequisites
- Python 3.10+
- Oracle Database (21c or later recommended)
- Oracle Instant Client (if using thick mode)

### 1. Clone the repository

```bash
git clone https://github.com/rslaanfareed/SkillSwap.git
cd SkillSwap
```

### 2. Install dependencies

```bash
pip install customtkinter oracledb python-dotenv bcrypt
```

### 3. Configure environment

Copy the example config and fill in your Oracle credentials:

```bash
cp config.example.env .env
```

```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=1521
DB_SERVICE=orcl
```

### 4. Set up the database

Run the SQL file in Oracle SQL Developer or SQL*Plus:

```sql
@SkillSwap.sql
```

This creates all tables, indexes, triggers, and loads sample data.

### 5. Set admin password

The seed data includes an admin account (`admin@skillswap.edu`) with a placeholder password hash. To set a real password, register a new account through the app first, then promote it to admin manually:

```sql
UPDATE USERS SET ROLE = 'ADMIN' WHERE EMAIL = 'your@email.com';
COMMIT;
```

### 6. Run the application

```bash
python main.py
```

---

## Sample Accounts (Seed Data)

All seed accounts use `CHANGE_IN_APP` as a placeholder hash. Set real passwords via the admin dashboard after logging in, or register fresh accounts.

| Name | Email | Role |
|---|---|---|
| Admin User | admin@skillswap.edu | ADMIN |
| Alice Johnson | alice@skillswap.edu | STUDENT |
| Bob Smith | bob@skillswap.edu | STUDENT |
| Carol Davis | carol@skillswap.edu | STUDENT |
| Dave Brown | dave@skillswap.edu | STUDENT |

---


