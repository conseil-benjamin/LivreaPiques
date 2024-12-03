SET SCHEMA 'public';

CREATE TABLE "user" (
  user_id           SERIAL       PRIMARY KEY,
  username          VARCHAR(30)  UNIQUE NOT NULL,
  password          VARCHAR(250),  -- Le mdp sera crypté
  age               INTEGER,
  gender            Gender       NOT NULL, 
  nb_book_per_year  INTEGER,
  nb_book_pleasure  INTEGER, 
  nb_book_work      INTEGER,
  initiated_by      VARCHAR(100) NOT NULL,
  reading_time      VARCHAR(20),
  choice_motivation VARCHAR(30)  NOT NULL
);

CREATE TABLE Book_Source ( 
  source_id     SERIAL        PRIMARY KEY,
  source_name  VARCHAR (100) NOT NULL
);

-- Association de user et de book_source
CREATE TABLE User_Book_Source (
  source_id   INTEGER,
  user_id     INTEGER,
  PRIMARY KEY (source_id, user_id),
  FOREIGN KEY (user_id) REFERENCES "User"(user_id),
  FOREIGN KEY (source_id) REFERENCES Book_Source(source_id)
);

CREATE TABLE Media (
  media_id   SERIAL      PRIMARY KEY,
  media_name VARCHAR(20) NOT NULL
);

-- La vérification pour le nombre de user_id dans la table sera faite grâce à un trigger
CREATE TABLE Fav_Medias (
  media_id INTEGER,
  user_id INTEGER,
  PRIMARY KEY (media_id, user_id),
  FOREIGN KEY (user_id) REFERENCES "User"(user_id),
  FOREIGN KEY (media_id) REFERENCES Media(media_id)
);

CREATE TABLE Liked_Publisher (
  user_id       INTEGER, 
  publisher_id  INTEGER,
  PRIMARY KEY (publisher_id, user_id),
  FOREIGN KEY (user_id) REFERENCES "User"(user_id),
  FOREIGN KEY (publisher_id) REFERENCES Publisher(publisher_id)
);

CREATE TABLE Liked_Genres (
  user_id  INTEGER,
  genre_id INTEGER,
  PRIMARY KEY (genre_id, user_id),
  FOREIGN KEY (user_id) REFERENCES "User"(user_id),
  FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
);

CREATE TABLE Liked_Series (
  series_id     INTEGER,
  user_id       INTEGER,
  PRIMARY KEY (series_id, user_id),
  FOREIGN KEY (user_id) REFERENCES "User"(user_id),
  FOREIGN KEY (series_id) REFERENCES Series(series_id)
);

CREATE TABLE Liked_Author (
  user_id   INTEGER,
  author_id INTEGER,
  PRIMARY KEY (author_id, user_id),
  FOREIGN KEY (user_id) REFERENCES "User"(user_id),
  FOREIGN KEY (author_id) REFERENCES Author(author_id)
);

CREATE TABLE Liked_Books (
  user_id   INTEGER,
  book_id   INTEGER,
  PRIMARY KEY (book_id, user_id),
  FOREIGN KEY (user_id) REFERENCES "User"(user_id),
  FOREIGN KEY (book_id) REFERENCES Book(book_id)
);

-- Trigger à mettre pour pas plus de trois, check si rank est au dessus de trois
CREATE TABLE Fav_Books (
  user_id   INTEGER,
  book_id   INTEGER,
  rank      INTEGER,
  PRIMARY KEY (book_id, user_id, rank),
  FOREIGN KEY (user_id) REFERENCES "User"(user_id),
  FOREIGN KEY (book_id) REFERENCES Book(book_id)
);

alter table "user" ALTER COLUMN nb_book_per_year TYPE VARCHAR(25);
alter table "user" ALTER COLUMN nb_book_pleasure TYPE VARCHAR(25);
alter table "user" ALTER COLUMN nb_book_work TYPE VARCHAR(10);
alter table "user" ALTER COLUMN initiated_by TYPE VARCHAR(100);
alter table "user" ALTER COLUMN choice_motivation TYPE VARCHAR(200);