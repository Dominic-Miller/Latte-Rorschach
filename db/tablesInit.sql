-- database 1st draft

-- designed for MySQL, consider Firebase/other in future if needed

DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Lattes;
DROP TABLE IF EXISTS Interpretations;
DROP TABLE IF EXISTS Comments;

-- can decide lengths once know values
-- how much role based access here vs Django built in?
-- change any names?

CREATE TABLE Users (
    userId        CHAR(10) PRIMARY KEY,
    userName      VARCHAR(20) NOT NULL,
    passwordHash  CHAR(10) NOT NULL
);

CREATE TABLE Lattes (
    latteId         CHAR(10) PRIMARY KEY,
    imgUrl          VARCHAR(50) NOT NULL,
    interpretCount  INT
);

CREATE TABLE Interpretations (
    interpretId  CHAR(10) PRIMARY KEY,
    userId       CHAR(10),
    latteId      CHAR(10),
    message      VARCHAR(200) NOT NULL,
    likes        INT,
    dislikes     INT,
    FOREIGN KEY (userId) REFERENCES Users(userId),
    FOREIGN KEY (latteId) REFERENCES Lattes(latteId)
);

CREATE TABLE Comments (
    userId       CHAR(10),
    interpretId  CHAR(10),
    message      VARCHAR(100) NOT NULL,
    FOREIGN KEY (userId) REFERENCES Users(userId),
    FOREIGN KEY (interpretId) REFERENCES Interpretations(interpretId)
);
