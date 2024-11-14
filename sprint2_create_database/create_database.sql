--create data base
CREATE DATABASE db_livreapique;

--create table
CREATE TABLE Book(
    book_id SERIAL PRIMARY KEY,
    book_title VARCHAR(280),
    nb_of_pages smallint,
    book_description VARCHAR(26770),
    settings VARCHAR(2540),
    isbn VARCHAR(30),
    isbn13 VARCHAR(200),
    original_title VARCHAR(280),
    review_count INT,
    one_star_rating INT,
    two_star_rating INT,
    three_star_rating INT,
    four_star_rating INT,
    five_star_rating INT,
    CONSTRAINT book_isbn_unique UNIQUE(isbn),
    CONSTRAINT book_isbn13_unique UNIQUE(isbn13)
);

CREATE TYPE Gender AS ENUM('M', 'F', 'A');

CREATE TABLE Author(
    author_id SERIAL PRIMARY KEY,
    author_name VARCHAR(200),
    author_gender Gender,
    birthplace VARCHAR(60)
    CONSTRAINT author_name_not_null CHECK(author_name IS NOT NULL)
);

CREATE TABLE Book_Author(
    book_id INT,
    author_id INT,
    PRIMARY KEY(book_id, author_id),
    FOREIGN KEY(book_id) REFERENCES Book(book_id),
    FOREIGN KEY(author_id) REFERENCES Author(author_id)
);

CREATE SEQUENCE smallint_sequence START 1 INCREMENT 1 MINVALUE 1 MAXVALUE 32767;

CREATE TABLE Publisher (
    publisher_id SMALLINT PRIMARY KEY DEFAULT nextval('smallint_sequence'),
    name_publisher VARCHAR(300),
    origin_publisher VARCHAR(60),
    CONSTRAINT name_publisher_unique UNIQUE(name_publisher),
    CONSTRAINT name_publisher_not_null CHECK(name_publisher IS NOT NULL)

);

CREATE TABLE Book_Publisher(
    book_id INT,
    publisher_id smallint,
    published_date DATE,
    published_title VARCHAR(280),
    PRIMARY KEY(book_id, publisher_id),
    FOREIGN KEY(book_id) REFERENCES Book(book_id),
    FOREIGN KEY(publisher_id) REFERENCES Publisher(publisher_id)
);

create table Genre(
    genre_id smallint PRIMARY KEY DEFAULT nextval('smallint_sequence'),
    genre_name VARCHAR(300)
    CONSTRAINT genre_name_not_null CHECK(genre_name IS NOT NULL),
    CONSTRAINT genre_name_unique UNIQUE(genre_name)
);

CREATE TABLE Book_Genre(
    book_id INT,
    genre_id smallint,
    nb_of_vote smallint,
    PRIMARY KEY(book_id, genre_id),
    FOREIGN KEY(book_id) REFERENCES Book(book_id),
    FOREIGN KEY(genre_id) REFERENCES Genre(genre_id)
);

CREATE TYPE Status AS ENUM ('completed', 'in progress', 'abandoned');

CREATE TABLE Series(
    series_id smallint PRIMARY KEY DEFAULT nextval('smallint_sequence'),
    series_name VARCHAR(105),
    series_status Status
    CONSTRAINT series_name_not_null CHECK(series_name IS NOT NULL),
    CONSTRAINT series_name_unique UNIQUE(series_name)
);

CREATE TABLE Book_Series(
    book_id INT,
    series_id smallint,
    PRIMARY KEY(book_id, series_id),
    FOREIGN KEY(book_id) REFERENCES Book(book_id),
    FOREIGN KEY(series_id) REFERENCES Series(series_id)
);

CREATE TABLE Awards(
    award_id smallint PRIMARY KEY DEFAULT nextval('smallint_sequence'),
    award_name VARCHAR(2240)
    CONSTRAINT award_name_not_null CHECK(award_name IS NOT NULL),
    CONSTRAINT award_name_unique UNIQUE(award_name)
);

CREATE TABLE Book_Awards(
    book_id INT,
    award_id smallint,
    date_award DATE,
    PRIMARY KEY(book_id, award_id),
    FOREIGN KEY(book_id) REFERENCES Book(book_id),
    FOREIGN KEY(award_id) REFERENCES Awards(award_id)
);

CREATE TABLE Character(
    character_id SERIAL PRIMARY KEY,
    character_name VARCHAR(200),
    book_id INT,
    FOREIGN KEY(book_id) REFERENCES Book(book_id)
);

CREATE VIEW Book_rating AS
SELECT 
    book_id, 
    book_title, 
    one_star_rating + two_star_rating + three_star_rating + four_star_rating + five_star_rating AS rating_count, 
    CASE 
        WHEN (one_star_rating + two_star_rating + three_star_rating + four_star_rating + five_star_rating) = 0 
        THEN NULL 
        ELSE ROUND(
            (one_star_rating*1 + two_star_rating*2 + three_star_rating*3 + four_star_rating*4 + five_star_rating*5) / 
            (one_star_rating + two_star_rating + three_star_rating + four_star_rating + five_star_rating * 1.0), 1
        )  -- Arrondir à une décimale
    END AS book_avg_rating
FROM Book
GROUP BY book_id, book_title;


CREATE OR REPLACE VIEW Author_avg_rating AS
SELECT 
    Author.author_id, 
    author_name, 
    LEAST(GREATEST(AVG(book_avg_rating), 0), 5) AS avg_rating
FROM 
    Book_Author
    JOIN Book_rating ON Book_Author.book_id = Book_rating.book_id
    JOIN Author ON Book_Author.author_id = Author.author_id
GROUP BY 
    Author.author_id, author_name;
