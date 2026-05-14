# Admin User Instructions

## System Purpose

This application is a staff-facing Pet Adoption Center Management System. It is designed for staff/admin users to manage pets, adopters, adoption applications, and finalized adoption records in one organized system.

## Accessing the Login Page

Open the application in a web browser and go to:

```text
http://127.0.0.1:5000
```
The system will direct you to the admin login page.

## Default Admin Credentials

Use the following default staff/admin account:

- Username: `admin`
- Password: `admin123`

After logging in, the system opens the dashboard.

## Dashboard Overview

The dashboard gives staff a quick summary of adoption center activity. It displays:

- Total pets
- Available pets
- Adopted pets
- Total applications
- Total adoption fees collected
- Average adoption fee

The dashboard also shows recent applications and recent finalized adoptions.

## Managing Pets

Use the Pets page to manage animal records.

Staff can:

- View all pets
- Add a new pet
- Edit pet information
- Delete a pet
- Review pet status and adoption fee
- See how many applications are linked to each pet

Required pet fields must be completed. Pet age and adoption fee cannot be negative.

## Managing Adopters

Use the Adopters page to manage people who apply to adopt pets.

Staff can:

- View all adopters
- Add a new adopter
- Edit adopter contact information
- Delete an adopter
- See how many applications are linked to each adopter

Required adopter fields must be completed. Email addresses must include `@`.

## Managing Applications

Use the Applications page to manage adoption requests.

Staff can:

- View all applications
- Add a new application
- Select the pet and adopter connected to the application
- Edit application status and notes
- Delete an application
- See whether an application has already been finalized as an adoption

Applications connect pets and adopters before an adoption is finalized.

## Finalizing an Adoption

To finalize an adoption, go to the Applications page and click the Finalize button for an eligible application.

When an adoption is finalized, the system performs these actions together:

- Creates a new adoption record
- Updates the pet status to `Adopted`
- Updates the application status to `Approved`

If any part of the transaction fails, the system rolls back the changes so the records stay consistent.

## Dashboard Statistics Updates

Dashboard statistics update based on the current database records.

For example:

- Adding or deleting pets changes total pet counts.
- Marking a pet as adopted changes available and adopted pet counts.
- Adding or deleting applications changes the total applications count.
- Finalizing adoptions updates total adoption fees and average adoption fee.

Refresh or revisit the dashboard after making changes to view the updated totals.

## Relationship Review

Use the Relationships page to review how pets, adopters, applications, and adoptions are connected. This page helps demonstrate the database relationships used by the management system.
