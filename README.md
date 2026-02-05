# Launchconnect

A Django-based platform for Students, Startups, and Founders.

## Prerequisites
- Python 3.11+
- PostgreSQL

## Setup & Run

1.  **Install Requirements**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Database Configuration**
    - Create a PostgreSQL database named `launchconnect`.
    - Update `launchconnect/settings.py` with your DB credentials if they differ from the default (`postgres`/`password`).

3.  **Run Migrations**
    ```bash
    python manage.py makemigrations users students startups jobs applications founder_collab
    python manage.py migrate
    ```

4.  **Create Superuser**
    ```bash
    python manage.py createsuperuser
    ```

5.  **Run Development Server**
    ```bash
    python manage.py runserver
    ```

## Features
- **Student Dashboard**: Apply for jobs, track status.
- **Startup Dashboard**: Post jobs, manage applicants (HTMX enabled).
- **Founder Network**: Post collaboration needs.
- **Admin**: Verify startups.

## Live Demo Credentials (Local)
Create users with different roles via the `/register/` page to test all flows.
