# Pet Adoption Center Management System

A beginner-friendly Flask full-stack DBMS Project 3 application for staff/admin use at a pet adoption center.

## Technology Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML
- CSS
- Bootstrap
- Jinja2

## Main Features

- Staff/admin login
- Dashboard with aggregate statistics
- CRUD for pets
- CRUD for adopters
- CRUD for adoption applications
- Finalized adoption records
- Relationship display across pets, adopters, applications, and adoptions
- Transaction workflow for finalizing an adoption
- Server-side validation for required fields, age, fees, and email format

## Login

Default demo account:

- Username: `admin1`
- Password: `pass123`

## How to Run

1. Create and activate a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Start the Flask app.

```bash
python app.py
```

4. Open the app in a browser.

```text
http://127.0.0.1:5000
```

The SQLite database is created automatically in the `instance` folder the first time the app runs.

## Database Tables

- `staff`
- `pet`
- `adopter`
- `application`
- `adoption`

## Finalize Adoption Transaction

When staff finalizes an application, the app performs these database operations as one transaction:

1. Creates an adoption record.
2. Updates the pet status to `Adopted`.
3. Updates the application status to `Approved`.
4. Rolls back all changes if an error occurs.

## Project Structure

```text
Project3_PetAdoption_App/
  app.py
  requirements.txt
  schema.sql
  README.md
  NORMALIZATION.md
  AI_LOG.md
  INSTRUCTIONS.md
  static/
    css/
      styles.css
  templates/
    base.html
    login.html
    dashboard.html
    relationships.html
    pets/
    adopters/
    applications/
    adoptions/
```
