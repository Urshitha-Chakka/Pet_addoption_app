CREATE TABLE staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(120) NOT NULL,
    full_name VARCHAR(120) NOT NULL
);

CREATE TABLE pet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(80) NOT NULL,
    breed VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Available',
    adoption_fee FLOAT NOT NULL DEFAULT 0
);

CREATE TABLE adopter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    address VARCHAR(200) NOT NULL
);

CREATE TABLE application (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER NOT NULL,
    adopter_id INTEGER NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Pending',
    notes TEXT NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pet (id),
    FOREIGN KEY (adopter_id) REFERENCES adopter (id)
);

CREATE TABLE adoption (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER NOT NULL,
    adopter_id INTEGER NOT NULL,
    application_id INTEGER NOT NULL UNIQUE,
    adoption_date DATE NOT NULL DEFAULT CURRENT_DATE,
    fee_paid FLOAT NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pet (id),
    FOREIGN KEY (adopter_id) REFERENCES adopter (id),
    FOREIGN KEY (application_id) REFERENCES application (id)
);

INSERT INTO staff (username, password, full_name)
VALUES ('admin', 'admin123', 'Admin Staff');
