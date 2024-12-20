create view user_taste as (
    SELECT 
    u.user_id, 
    u.username, 
    lb.book_id AS liked,
    b.book_title AS title_liked,
    NULL AS fav,
    NULL AS title_fav
FROM "user" u
LEFT JOIN liked_books lb ON u.user_id = lb.user_id
LEFT JOIN book b ON lb.book_id = b.book_id

UNION

SELECT 
    u.user_id, 
    u.username, 
    NULL AS liked,
    NULL AS title_liked,
    fb.book_id AS fav,
    b.book_title AS title_fav
FROM "user" u
LEFT JOIN fav_books fb ON u.user_id = fb.user_id
LEFT JOIN book b ON fb.book_id = b.book_id
WHERE fb.book_id NOT IN (SELECT book_id FROM liked_books WHERE user_id = u.user_id)

)
