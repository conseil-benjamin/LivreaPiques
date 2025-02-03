import pandas as pd
from math import sqrt
from supabase import create_client, Client
from sklearn.preprocessing import MinMaxScaler

url = "https://pczyoeavtwijgtkzgcaz.supabase.co"
key ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBjenlvZWF2dHdpamd0a3pnY2F6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzEzOTc1NTUsImV4cCI6MjA0Njk3MzU1NX0._KJBbSHWivEF6VrPdyO3TUI729c0eXnj-zoVeQmFYQc"

# Set display options for full display
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def recommend_books(key, url, userid, n):
    '''
        key: API key of the database
        url: The URL of the Database
        userid: The ID of the user
        n: The number of elements you want to be returned
    '''
    # Call to function to transform the values to usable ones
    BookDf = Transform(url, key)
    # Create a client to connect to the database
    supabase: Client = create_client(url, key)
    # Fetch the data to get the liked books of the user 
    response = supabase.table('liked_books').select('book_id').eq("user_id", userid).execute()
    # Transform the returned object to a list
    BookLiked = [item['book_id'] for item in response.data]
    # To delete
    BookLiked = [10, 9462]
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
    BookDf, GenreDf, AuthorDf, PublisherDf, RatingDf = getData(url, key)
    #Book table
    BookDf.set_index("book_id", inplace=True)
    BookDf = BookDf.drop("isbn", axis=1)
    BookDf = BookDf.drop("isbn13", axis=1)
    BookDf = BookDf.drop("book_title", axis=1)
    BookDf = BookDf.drop("book_description", axis=1)
    BookDf = BookDf.drop("original_title", axis=1)
    BookDf = BookDf.drop("one_star_rating", axis=1)
    BookDf = BookDf.drop("two_star_rating", axis=1)
    BookDf = BookDf.drop("three_star_rating", axis=1)
    BookDf = BookDf.drop("four_star_rating", axis=1)
    BookDf = BookDf.drop("five_star_rating", axis=1)
    # One hot encoding (With true and false values)
    BookDf = pd.get_dummies(BookDf)
    # Convert booleans to float
    BookDf = BookDf.astype(float)    
    BookDf = BookDf.fillna(0)
    #BookDf = (BookDf-BookDf.mean())/BookDf.std()
    #table book-genre and genre
    GenreDf.set_index("book_id", inplace=True)
    GenreDf = GenreDf.drop(columns="nb_of_vote")
    GenreDf = GenreDf.drop(columns="genre_id")
    GenreDf = pd.get_dummies(GenreDf)
    GenreDf = GenreDf.groupby("book_id").any()
    #table book_author author
    AuthorDf.set_index("book_id", inplace=True)
    AuthorDf = AuthorDf.drop(columns="author_id")
    AuthorDf = pd.get_dummies(AuthorDf)
    AuthorDf = AuthorDf.groupby("book_id").any()
    #table book_publisher 
    PublisherDf.set_index("book_id", inplace=True)
    PublisherDf = PublisherDf.drop(columns="published_date")
    PublisherDf = PublisherDf.drop(columns="published_title")
    PublisherDf = PublisherDf.drop(columns="publisher_id")
    PublisherDf = pd.get_dummies(PublisherDf)
    PublisherDf = PublisherDf.groupby("book_id").any()
    # Table Book Rating
    RatingDf.set_index("book_id", inplace=True)
    #Treatment to form the final table and values
    BookDf = BookDf.join(GenreDf)
    BookDf = BookDf.join(AuthorDf)
    BookDf = BookDf.join(PublisherDf)
    BookDf = BookDf.join(RatingDf)
    BookDf = BookDf.fillna(0)
    # apply normalization techniques on Column 1 
    column = 'nb_of_pages'
    BookDf[column] = BookDf[column] /BookDf[column].abs().max() 
    return BookDf
    
def getData(url, key):
    supabase: Client = create_client(url, key)
    response = supabase.table("book").select("*").order("book_id", desc=False).execute()
    BookDf = pd.DataFrame(response.data)
    response = supabase.table('book_genre').select('*, genre(genre_name)').order("book_id", desc=False).execute()
    GenreDf = pd.DataFrame(response.data)
    GenreDf['genre'] = GenreDf['genre'].apply(lambda x: x.get('genre_name') if isinstance(x, dict) else None)
    response = supabase.table('book_author').select('*, author(author_name)').order("book_id", desc=False).execute()
    AuthorDf = pd.DataFrame(response.data)
    AuthorDf['author'] = AuthorDf['author'].apply(lambda x: x.get('author_name') if isinstance(x, dict) else None)
    response = supabase.table('book_publisher').select('*, publisher(name_publisher)').order("book_id", desc=False).execute()
    PublisherDf = pd.DataFrame(response.data)
    PublisherDf['publisher'] = PublisherDf['publisher'].apply(lambda x: x.get('name_publisher') if isinstance(x, dict) else None)
    response = supabase.table('book_rating').select('book_id, book_avg_rating').order("book_id", desc=False).execute()
    RatingDf = pd.DataFrame(response.data)
    print(RatingDf.head())
    return BookDf, GenreDf, AuthorDf, PublisherDf, RatingDf

print(recommend_books(key, url, 7, 5))
