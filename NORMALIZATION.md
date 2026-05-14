# Normalization Notes

## First Normal Form (1NF)

Each table uses atomic fields. For example, pet information is stored as separate fields such as name, species, breed, age, status, and adoption fee. Repeating groups are avoided.

## Second Normal Form (2NF)

Each table has a single-column primary key, and all non-key columns depend on that table's primary key. For example, adopter email, phone, and address depend only on the adopter record.

## Third Normal Form (3NF)

The design avoids storing derived or unrelated data in the wrong table. Pet details are stored in the pet table, adopter details are stored in the adopter table, and application details connect a pet to an adopter.

## Relationship Design

- One pet can have many applications.
- One adopter can submit many applications.
- One application belongs to one pet and one adopter.
- One finalized adoption is linked to one application.
- One finalized adoption also references the adopted pet and adopter.

## Why Separate Applications and Adoptions?

Applications represent the request or review process. Adoptions represent completed adoption transactions. Keeping them separate prevents mixing pending requests with finalized adoption records.

## Transaction Requirement

Finalizing an adoption changes multiple tables. The app uses one database transaction so the adoption record, pet status, and application status remain consistent.
