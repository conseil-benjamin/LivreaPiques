-- table book et cie
create index idx_book_book_id
ON book(book_id);

create index idx_book_book_title
ON book(book_title);

create index idx_book_book_cover
ON book(book_cover);

create index idx_book_book_description
ON book(book_description);

create index idx_book_awards_book_id
ON book_awards(book_id);

create index idx_book_genre_genre_id
ON book_genre(genre_id);

create index idx_book_rating_book_id
ON book_rating(book_id);

create index idx_book_series_book_id
ON book_series(book_id);

--table author et cie
create index idx_book_author_author_id
ON book_author(author_id);

create index idx_author_author_id
ON author(author_id);


-- autres tables servant aux recherches
create index idx_awards_award_id
ON awards(award_id);

create index idx_genre_genre_id
ON genre(genre_id);

create index idx_series_series_id
ON series(series_id);
