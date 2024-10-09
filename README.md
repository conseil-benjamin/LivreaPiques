### Big_boss_authors Table
|QualitatativeVariable|Quantitative Variable|No data(index, or joined data)|
|---    |:-:    |:-:    |
|author_gender|author_average_rating|author_id
|author_genres|author_review_count|author_name
|birthplace|author_rating_count|book_id
|genre_1|book_average_rating|book_title
|genre_2|num_ratings|
|       |num_reviews|
|       |pages|
|       |publish_date|

### bigboss_book Table
|QualitatativeVariable|Quantitative Variable|No data(index, or joined data)|
|---    |:-:    |:-:    |
|series|rating_count|id
|publisher|review_count|title
|genre_and_votes|average_rating|author
|settings|five_star_ratings|original_title
|characters|four_star_ratings|isbn
|awards|three_star_ratings|isbn13
|books_in_series|two_star_ratings|description
||one_star_ratings|
||number_of_pages|
||date_published|
|||

## Explanation of the various variables of the data sets
### Authors table
**author_gender** : Man or Woman

**author_average_rating** : Average rating of each books the author wrote

**author_genres** : Main genres of an Author

**author_name** : The name of the author

**author_rating_count** : The number of rating the author received (One issue that we encountered is the fact that some of the values of said variable can be different for the same author and we can suppose that it is due to the data being older so he/she received more votes after the the first appearence)

**author_review_count** :  The number of review received by the author (Same issue as the before mentioned variable)

**birthplace** : The *country* where the author is born

**book_average_rating** : The average rating of the book

**book_title** : The title of the book (Obviously)

**genre_1** : The principal genre of the book


**genre_2** : The audience targetted by the book

**num_ratings** : The number of rating received by the book

**num_reviews** : The number of review received by the book

**pages** : The total of pages in the book

**publish_date** : Date on where the book was published

### Table livres

**title** : The title of the book (Obviously)

**series** : The series of the books of which it is a part of

**author** : The book's authoer

**rating_count** : Count of the rating cumuled by the book

**review_count** : Count of the review cumuled by the book

**average_rating** : Book's average rating

**five_star_ratings** : Numbers of five start ratings

**number_of_pages** : The total of pages in the book

**date_published** : Date on where the book was published

**publisher** : Name of who published the book

**original_title** : Original title (if not false)

**genre_and_votes** : The genre of the book and the number of people that voted for it

**isbn**, **isbn13** : The unique identifier of the book

**settings** : Where does the story of the books take place

**characters** : The characters present in the book

**awards** : Name of the award (if the book has one) the book won

**books_in_series** : Other books in the series characterized by their id or isbn

**description** : A description/summary of the book







