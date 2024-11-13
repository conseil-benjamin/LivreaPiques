--create data base
CREATE DATABASE db_livreapique;

--create table
CREATE TABLE Book(
    id_book SERIAL PRIMARY KEY,
    title VARCHAR(280),
    nb_pages smallint,
    description VARCHAR(26770),
    settings VARCHAR(50),
    isbn VARCHAR(30),
    isbn13 VARCHAR(30),
    original_title VARCHAR(280),
    review_count INT,
    one_star_rating INT,
    two_star_rating INT,
    three_star_rating INT,
    four_star_rating INT,
    five_star_rating INT,
    rating_count INT CHECK(rating_count = one_star_rating + two_star_rating + three_star_rating + four_star_rating + five_star_rating),
    average_rating FLOAT CHECK(average_rating = one_star_rating*1 + two_star_rating*2 + three_star_rating*3 + four_star_rating*4 + five_star_rating*5 / rating_count)

);

CREATE TYPE Gender AS ENUM('M', 'F', 'A');

CREATE TABLE Author(
    id_author SERIAL PRIMARY KEY,
    name_author VARCHAR(50),
    author_gender Gender,
    birthplace VARCHAR(50)
);

CREATE TABLE Book_Author(
    id_book INT,
    id_author INT,
    PRIMARY KEY(id_book, id_author),
    FOREIGN KEY(id_book) REFERENCES Book(id_book),
    FOREIGN KEY(id_author) REFERENCES Author(id_author)
);

CREATE SEQUENCE smallint_sequence START 1 INCREMENT 1 MINVALUE 1 MAXVALUE 32767;

CREATE TABLE Publisher (
    id_publisher SMALLINT PRIMARY KEY DEFAULT nextval('smallint_sequence'),
    name_publisher VARCHAR(50),
    origin_publisher VARCHAR(50)
);

CREATE TABLE Book_Publisher(
    id_book INT,
    id_publisher smallint,
    date_published DATE,
    title_published VARCHAR(280),
    PRIMARY KEY(id_book, id_publisher),
    FOREIGN KEY(id_book) REFERENCES Book(id_book),
    FOREIGN KEY(id_publisher) REFERENCES Publisher(id_publisher)
);

create table Genre(
    id_genre smallint PRIMARY KEY DEFAULT nextval('smallint_sequence'),
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
    id_series smallint PRIMARY KEY DEFAULT nextval('smallint_sequence'),
    name_series VARCHAR(105),
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
    id_award smallint PRIMARY KEY DEFAULT nextval('smallint_sequence'),
    name_award VARCHAR(2240)
);

CREATE TABLE Book_Awards(
    id_book INT,
    id_award smallint,
    PRIMARY KEY(id_book, id_award),
    FOREIGN KEY(id_book) REFERENCES Book(id_book),
    FOREIGN KEY(id_award) REFERENCES Awards(id_award)
);