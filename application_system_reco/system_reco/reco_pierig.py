import pandas as pd
from math import sqrt
from supabase import create_client, Client
from sklearn.preprocessing import MinMaxScaler
from SQL_controleur.SQL_controleur import *


url = "https://pczyoeavtwijgtkzgcaz.supabase.co"
key ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBjenlvZWF2dHdpamd0a3pnY2F6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzEzOTc1NTUsImV4cCI6MjA0Njk3MzU1NX0._KJBbSHWivEF6VrPdyO3TUI729c0eXnj-zoVeQmFYQc"



def recommend_books(userid, key=key, url=url, n=5):
    '''
        key: API key of the database
        url: The URL of the Database
        userid: The ID of the user
        n: The number of elements you want to be returned
    '''
    # Call to function to transform the values to usable ones
    BookDf = Transform(url, key)
    # Create a client to connect to the database
    #supabase: Client = create_client(url, key)
    # Fetch the data to get the liked books of the user 
    #response = supabase.table('liked_books').select('book_id').eq("user_id", userid).execute()
    response = requete("SELECT book_id FROM liked_books WHERE user_id = " + str(userid))

    # Transform the returned object to a list
    BookLiked = response.values.flatten().tolist()

    # Get the average book liked by the user
    MeanOfLikedBooks = MeanOfBooksRead(BookLiked, BookDf)
    # List of euclidean distance
    DistanceList = []
    # Reset the index to make a list
    BookDf.reset_index(drop=False, inplace=True)
    # One hot encoding (With true and false values)
    BookDf = pd.get_dummies(BookDf)
    # Convert booleans to float
    BookDf = BookDf.astype(float)
    # Conversion to a list
    BookList = BookDf.values.tolist()
    # For each books in all the books
    for Book in BookList:
        # We avoid the book already liked
        if (Book[0] in BookLiked):
            continue
        # Continuation of the program with condition of not having an empty list
        elif (Book != []):
            # Definition of the sum variable
            sum = 0
            # For elements in the Average book
            for i in range(len(MeanOfLikedBooks)):
                # We do the sum of Book minus the same value in the Average vector then we get the absolute value by raising it to 2
                sum = sum + (Book[i+1] - MeanOfLikedBooks[i])**2
            # We add at the end of the list a tuple of the id of the book and the and the square root of the sum to get the euclidean distance 
            DistanceList.append((Book[0],(sqrt(sum))))
    # Sort the list by distance
    DistanceList.sort(key=lambda x: x[1])
    # Returns the n first element of the list
    return DistanceList[:n]

def MeanOfBooksRead(ListOfBooksIds, BookDf):
    # Calculate the Average book 
    mean = 0
    # One hot encoding (With true and false values)
    BookDf = pd.get_dummies(BookDf)
    # Convert booleans to float
    BookDf = BookDf.astype(float)
    # For every book in the book list
    for BookId in ListOfBooksIds:
        # We fetch the book in the book dataframe
        BaseBook = BookDf.loc[BookId].values.tolist()
        # If mean is equal to 0 then we take the values of the selected book
        if(mean == 0):
            mean = BaseBook
        # Else we calculate the average value of the book
        else:
            mean = [(mean[i] + BaseBook[i]) for i in range(len(mean))]
    return mean


def Transform(url, key):
    requeteAll = """
        SELECT 
            book.book_id,
            book.settings,
            book.nb_of_pages,
            book.review_count,
            book_rating.book_avg_rating,
            NULLIF(authors.listAuthor, '') AS listAuthor, 
            NULLIF(publishers.listePublisher, '') AS listePublisher, 
            NULLIF(genres.listeGenre, '') AS listeGenre
        FROM book
        LEFT JOIN (
            SELECT book_author.book_id, STRING_AGG(author.author_name, ', ') AS listAuthor
            FROM book_author
            JOIN author ON author.author_id = book_author.author_id
            GROUP BY book_author.book_id
        ) AS authors ON book.book_id = authors.book_id
        LEFT JOIN (
            SELECT book_publisher.book_id, STRING_AGG(publisher.name_publisher, ', ') AS listePublisher
            FROM book_publisher
            JOIN publisher ON publisher.publisher_id = book_publisher.publisher_id
            GROUP BY book_publisher.book_id
        ) AS publishers ON book.book_id = publishers.book_id
        LEFT JOIN (
            SELECT book_genre.book_id, STRING_AGG(genre.genre_name, ', ') AS listeGenre
            FROM book_genre
            JOIN genre ON genre.genre_id = book_genre.genre_id
            GROUP BY book_genre.book_id
        ) AS genres ON book.book_id = genres.book_id
        LEFT JOIN book_rating ON book.book_id = book_rating.book_id
        """
    BookDf = requete(requeteAll)
    print(BookDf.head)
    # transformer listegenre qui contient [genre1, genre2, genre3] en genre1, genre2, genre3
    BookDf['listegenre'] = BookDf['listegenre'].apply(lambda x: x.split(', ') if x != None else [])
    BookDf['listeauthor'] = BookDf['listeauthor'].apply(lambda x: x.split(', ') if x != None else [])
    BookDf['listepublisher'] = BookDf['listepublisher'].apply(lambda x: x.split(', ') if x != None else [])
    print(BookDf.head)
    BookDf = BookDf.fillna(0)
    # apply normalization techniques on Column 1 
    column = 'nb_of_pages'
    BookDf[column] = BookDf[column] /BookDf[column].abs().max() 
    return BookDf
    
def getData(url, key):
    #supabase: Client = create_client(url, key)
    #response = supabase.table("book").select("*").order("book_id", desc=False).execute()
    #BookDf = pd.DataFrame(response.data)
    BookDf = requete("SELECT * FROM book ORDER BY book_id")

    #response = supabase.table('book_genre').select('*, genre(genre_name)').order("book_id", desc=False).execute()
    #GenreDf = pd.DataFrame(response.data)
    GenreDf = requete("SELECT book_genre.*, genre.genre_name as genre FROM book_genre natural join genre ORDER BY book_genre.book_id ASC")
    
    #response = supabase.table('book_author').select('*, author(author_name)').order("book_id", desc=False).execute()
    #AuthorDf = pd.DataFrame(response.data)
    AuthorDf = requete("SELECT book_author.*, author.author_name as author FROM book_author natural join author ORDER BY book_author.book_id ASC")

    #response = supabase.table('book_publisher').select('*, publisher(name_publisher)').order("book_id", desc=False).execute()
    #PublisherDf = pd.DataFrame(response.data)
    PublisherDf = requete("SELECT book_publisher.*, publisher.name_publisher FROM book_publisher natural join publisher ORDER BY book_publisher.book_id ASC")
    
    #response = supabase.table('book_rating').select('book_id, book_avg_rating').order("book_id", desc=False).execute()
    #RatingDf = pd.DataFrame(response.data)
    RatingDf = requete("SELECT book_id, book_avg_rating FROM book_rating ORDER BY book_id")
    print(RatingDf.head())
    return BookDf, GenreDf, AuthorDf, PublisherDf, RatingDf

