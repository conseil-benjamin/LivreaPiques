import sys
sys.path.append("./sprint2_populating/application/")

from SQL_controleur import requete

from Populate.Book import __main__ as populate_book
from Populate.Character import __main__ as populate_character
from Populate.Series import __main__ as populate_series
from Populate.Award import __main__ as populate_award
from Populate.Publisher import __main__ as populate_publisher
from Populate.Author import __main__ as populate_author
from Populate.Genre import __main__ as populate_genre
from time import sleep

from sprint2_populating_Alt.user import __main__ as populate_user
from sprint2_populating_Alt.book_source import __main__ as populate_book_source
from sprint2_populating_Alt.reading_mean import __main__ as populate_mean
from sprint2_populating_Alt.media import __main__ as populate_media
from sprint2_populating_Alt.Populate.liked_genre import __main__ as populate_liked_genre

from sprint2_populating_Alt.Populate.Book.Book import __main__ as new_populate_book
from sprint2_populating_Alt.Populate.Book.Genre import __main__ as new_populate_genre
from sprint2_populating_Alt.Populate.Book.Publisher import __main__ as new_populate_publisher
from sprint2_populating_Alt.likes_book import __main__ as populate_like_book

def populate():
    """
    This function is the main function of the application. It calls the main functions of all the modules to populate the database.

    Returns:
        bool: True if the database is populated successfully, False otherwise.

    Raises:
        Exception: If an error occurs while populating the database.
    """
    res = requete("select book_id from book where book_id = \"a\"")
    if res != None:
        try:
            print('populate_liked_genre')
            populate_liked_genre()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False

        try:
            populate_book()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False
        
        try:
            populate_character()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False

        try:
            populate_series()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False
        
        try:
            populate_award()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False
        
        try:
            populate_publisher()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False
        
        try:
            populate_author()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False

        try:
            populate_genre()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False

        try:
            populate_user()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False
        try:
            populate_book_source()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False
        try:
            populate_mean()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False
        try:
            populate_media()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False
        try:
            new_populate_book()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False
        try:
            new_populate_genre()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False
        try:
            new_populate_publisher()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False
        try:
            populate_like_book()
        except Exception as e:
            print(f"Error while populating the database: {e}")
            return False

        return True
    else:
        print('Database already populated')
        return False

