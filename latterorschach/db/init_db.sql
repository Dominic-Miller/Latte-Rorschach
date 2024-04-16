-- Ensure the LatteRorschach database is created and used
CREATE DATABASE IF NOT EXISTS LatteRorschach;
USE LatteRorschach;

-- Remove tables if they exist already
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Interpretations;
DROP TABLE IF EXISTS Lattes;
DROP TABLE IF EXISTS Users;

-- Create Users table
CREATE TABLE Users (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    userName      VARCHAR(20) NOT NULL,
    passwordHash  CHAR(255) NOT NULL
);

-- Create Lattes table
CREATE TABLE Lattes (
    latteId         CHAR(10) PRIMARY KEY,
    imgUrl          VARCHAR(50) NOT NULL,
    interpretCount  INT DEFAULT 0
);

-- Create Interpretations table
CREATE TABLE Interpretations (
    interpretId  CHAR(10) PRIMARY KEY,
    userId       INT,
    latteId      CHAR(10),
    message      VARCHAR(200) NOT NULL,
    likes        INT DEFAULT 0,
    dislikes     INT DEFAULT 0,
    FOREIGN KEY (userId) REFERENCES Users(userId),
    FOREIGN KEY (latteId) REFERENCES Lattes(latteId)
);

-- Create Comments table
CREATE TABLE Comments (
    userId       INT, 
    interpretId  CHAR(10),
    message      VARCHAR(100) NOT NULL,
    FOREIGN KEY (userId) REFERENCES Users(userId),
    FOREIGN KEY (interpretId) REFERENCES Interpretations(interpretId)
);

-- Print success message
SELECT 'Database and tables created successfully.' AS Message;

-- To initialize this database: mysql -u root -p < init_db.sql
