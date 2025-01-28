import pandas as pd
from math import sqrt
from supabase import create_client, Client

url = "https://pczyoeavtwijgtkzgcaz.supabase.co"
key ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBjenlvZWF2dHdpamd0a3pnY2F6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzEzOTc1NTUsImV4cCI6MjA0Njk3MzU1NX0._KJBbSHWivEF6VrPdyO3TUI729c0eXnj-zoVeQmFYQc"

# Set display options for full display
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def recommend_books(key, url, userid, n):
    BookDf = Transform(url, key)
    supabase: Client = create_client(url, key)
    response = supabase.table('liked_books').select('book_id').eq("user_id", userid).execute()
    BookLiked = [item['book_id'] for item in response.data]
    BookLiked = [1, 2]
    MeanOfLikedBooks = MeanOfBooksRead(BookLiked, BookDf)
    DistanceList = []
    BookDf.reset_index(drop=False, inplace=True)
    BookDf = pd.get_dummies(BookDf)
    BookDf = BookDf.astype(float)
    BookList = BookDf.values.tolist()
    response = supabase.table('liked_books').select('book_id').eq("user_id", userid).execute()
    for Book in BookList:
        if (Book[0] in BookLiked):
            continue
        elif (Book != []):
            sum = 0
            for i in range(len(MeanOfLikedBooks)):
                sum = sum + (Book[i+1] - MeanOfLikedBooks[i])**2
            DistanceList.append((Book[0],(sqrt(sum))))
    DistanceList.sort(key=lambda x: x[1])
    return DistanceList[:n]

def MeanOfBooksRead(ListOfBooksIds, BookDf):
    mean = 0
    BookDf = pd.get_dummies(BookDf)
    BookDf = BookDf.astype(float)
    for BookId in ListOfBooksIds:
        BaseBook = BookDf.loc[BookId].values.tolist()
        if(mean == 0):
            mean = BaseBook
        else:
            mean = [(mean[i] + BaseBook[i]) for i in range(len(mean))]
    return mean


def Transform(url, key):
    BookDf, GenreDf, AuthorDf, PublisherDf = getData(url, key)
    #Book table
    BookDf.set_index("book_id", inplace=True)
    BookDf = BookDf.drop("isbn", axis=1)
    BookDf = BookDf.drop("isbn13", axis=1)
    BookDf = BookDf.drop("book_title", axis=1)
    BookDf = BookDf.drop("book_description", axis=1)
    BookDf = BookDf.drop("original_title", axis=1)
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
    #Treatment to form the final table and values
    BookDf = BookDf.join(GenreDf)
    BookDf = BookDf.join(AuthorDf)
    BookDf = BookDf.join(PublisherDf)
    BookDf = BookDf.fillna(0)
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
    return BookDf, GenreDf, AuthorDf, PublisherDf

print(recommend_books(key, url, 1, 5))
