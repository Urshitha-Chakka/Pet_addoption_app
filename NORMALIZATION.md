# Normalization Notes

## First Normal Form (1NF)

The database satisfies First Normal Form because all tables contain atomic values and each column stores only a single piece of information. Repeating groups and multi-valued attributes are avoided.

For example, the `pets` table stores pet information in separate columns such as:
- pet_name
- species
- breed
- gender
- age
- adoption_status

Instead of storing multiple breeds, statuses, or adopter information inside one column, each value is stored individually. This makes the data easier to search, update, and manage.

---

## Second Normal Form (2NF)

The database satisfies Second Normal Form because every table uses a single-column primary key, and all non-key attributes depend entirely on that key.

For example:
- In the `adopters` table, fields such as email, phone number, city, and state depend only on the `adopter_id`.
- In the `pets` table, pet attributes such as breed, species, and age depend only on the `pet_id`.

There are no partial dependencies because the tables do not use composite primary keys for storing unrelated attributes.

---

## Third Normal Form (3NF)

The database satisfies Third Normal Form because non-key attributes depend only on the primary key and not on other non-key attributes.

Information is separated into appropriate tables to reduce redundancy and improve data integrity.

Examples:
- Pet details are stored only in the `pets` table.
- Adopter details are stored only in the `adopters` table.
- Application information is stored in the `applications` table.
- Adoption transaction records are stored separately in the `adoptions` table.

This design prevents duplicate data and reduces update, insertion, and deletion anomalies.

For example:
- Updating an adopter phone number only requires changing one record in the `adopters` table.
- Pet information does not need to be repeated inside every application record.
- Removing an application does not delete the pet or adopter information from the database.

---

## Relationship Design

The application uses relational database relationships to connect the different entities in the system.

### Relationships Included

- One pet can have many applications.
- One adopter can submit many applications.
- Each application belongs to one pet and one adopter.
- One finalized adoption belongs to one application.
- One adoption record references the adopted pet and adopter.

These relationships are maintained using primary keys and foreign keys to ensure referential integrity.

---

## Why Applications and Adoptions Are Separate

Applications and adoptions are stored in separate tables because they represent different stages of the adoption process.

The `applications` table is used for:
- pending requests
- approved requests
- rejected requests

The `adoptions` table is used only for completed adoptions.

Keeping them separate helps maintain clearer business logic and prevents incomplete or rejected applications from being mixed with finalized adoption records.

---

## Transaction Requirement

Finalizing an adoption requires updating multiple tables at the same time.

When an adoption is finalized:
1. A new adoption record is created.
2. The selected pet status changes to "Adopted."
3. The related application status changes to "Approved."

These operations are handled using a single database transaction. If one step fails, the entire transaction is rolled back to prevent inconsistent or incomplete data from being stored in the database.

This helps maintain data integrity throughout the application.