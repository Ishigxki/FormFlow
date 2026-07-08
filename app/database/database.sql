CREATE DATABASE formflow_db;
USE formflow_db;


CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL

);

CREATE TABLE Student_Profile(
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    university VARCHAR(100) NOT NULL,
    degree VARCHAR(100) NOT NULL,
    graduation_year INTEGER NOT NULL,
    bio VARCHAR(255)

    FOREIGN KEY (user_id) REFERENCES Users(id)

);

CREATE TABLE Opportunities(
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    company VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL,
    deadline DATE,
    description VARCHAR(100) NOT NULL,
    application_link VARCHAR(100) NOT NULL

);

CREATE TABLE Applications(
    id SERIAL PRIMARY KEY,
    student_id INTEGER,
    opportunity_id INTEGER,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    FOREIGN KEY (student_id) REFERENCES Student_Profile(id),
    FOREIGN KEY (opportunity_id) REFERENCES Oppotunities(id)
);