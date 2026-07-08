CREATE DATABASE formflow_db;
USE formflow_db;


CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at DATE NOT NULL

);

CREATE TABLE Student_Profile(
    id INTEGER PRIMARY KEY,
    user_id INTEGER ,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    university VARCHAR(100) NOT NULL,
    degree VARCHAR(100) NOT NULL,
    graduation_year INTEGER NOT NULL,
    bio VARCHAR(255)

    FOREIGN KEY (user_id) REFERENCES Users(id)

);

CREATE TABLE Opportunities(
    id INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    company VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL,
    deadline DATE,
    description VARCHAR(100) NOT NULL,
    application_link VARCHAR(100) NOT NULL

);

CREATE TABLE Applications(
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    opportunity_id INTEGER,
    status VARCHAR(20) NOT NULL,
    created_at Date NOT NULL,
    updated_at DATE NOT NULL
);