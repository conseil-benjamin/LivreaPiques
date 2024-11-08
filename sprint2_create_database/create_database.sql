--create data base
CREATE DATABASE db_livreapique;
--use data base
USE db_livreapique;

--create table
CREATE TABLE Book(
    id_book INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    nb_pages smallint,
    description VARCHAR(100),
    -- settings?
    isbn INT,
    isbn13 INT,
    original_title VARCHAR(50),
);

CREATE TABLE Author(
    id_author INT PRIMARY KEY AUTO_INCREMENT,
    name_author VARCHAR(50),
    author_gender VARCHAR(10),
    birthplace VARCHAR(50)
);

CREATE TABLE Book_Author(
    id_book INT,
    id_author INT,
    PRIMARY KEY(id_book, id_author),
    FOREIGN KEY(id_book) REFERENCES Book(id_book),
    FOREIGN KEY(id_author) REFERENCES Author(id_author)
);

CREATE TABLE Publisher(
    id_publisher smallint PRIMARY KEY AUTO_INCREMENT,
    name_publisher VARCHAR(50),
    origin_publisher VARCHAR(50)
);

CREATE TABLE Book_Publisher(
    id_book INT,
    id_publisher smallint,
    date_published DATE,
    title_published VARCHAR(50),
    PRIMARY KEY(id_book, id_publisher),
    FOREIGN KEY(id_book) REFERENCES Book(id_book),
    FOREIGN KEY(id_publisher) REFERENCES Publisher(id_publisher)
);

create table Genre(
    id_genre smallint PRIMARY KEY AUTO_INCREMENT,
    name_genre VARCHAR(50)
);

CREATE TABLE Book_Genre(
    id_book INT,
    id_genre smallint,
    nb_vote smallint,
    PRIMARY KEY(id_book, id_genre),
    FOREIGN KEY(id_book) REFERENCES Book(id_book),
    FOREIGN KEY(id_genre) REFERENCES Genre(id_genre)
);

CREATE TYPE Status AS ENUM ('completed', 'in progress', 'abandoned');

CREATE TABLE Series(
    id_series smallint PRIMARY KEY AUTO_INCREMENT,
    name_series VARCHAR(50),
    status_series Status
);

CREATE TABLE Book_Series(
    id_book INT,
    id_series smallint,
    PRIMARY KEY(id_book, id_series),
    FOREIGN KEY(id_book) REFERENCES Book(id_book),
    FOREIGN KEY(id_series) REFERENCES Series(id_series)
);

CREATE TABLE Awards(
    id_award smallint PRIMARY KEY AUTO_INCREMENT,
    name_award VARCHAR(100),
);

CREATE TABLE Book_Awards(
    id_book INT,
    id_award smallint,
    PRIMARY KEY(id_book, id_award),
    FOREIGN KEY(id_book) REFERENCES Book(id_book),
    FOREIGN KEY(id_award) REFERENCES Awards(id_award)
);



