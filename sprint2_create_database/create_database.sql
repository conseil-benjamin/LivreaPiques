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