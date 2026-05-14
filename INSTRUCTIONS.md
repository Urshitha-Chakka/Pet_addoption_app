# Instructions

## Setup

Open a terminal in the project folder.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Login

- Username: `admin`
- Password: `admin123`

## Testing Checklist

- Log in as admin.
- Add, edit, and delete a pet.
- Add, edit, and delete an adopter.
- Add, edit, and delete an application.
- Try invalid data:
  - Empty required fields
  - Negative pet age
  - Negative adoption fee
  - Email without `@`
- Finalize an adoption from the Applications page.
- Confirm the pet status changes to `Adopted`.
- Confirm the application status changes to `Approved`.
- Confirm an adoption record appears on the Adoptions page.
- Check dashboard statistics.
- Check relationship display page.

## Resetting the Database

Stop the Flask server, delete the SQLite database file in the `instance` folder, and run `python app.py` again.
