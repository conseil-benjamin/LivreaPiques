from Populate.Book import __main__ as populate_book
from Populate.Character import __main__ as populate_character
from Populate.Series import __main__ as populate_series
from Populate.Award import __main__ as populate_award
from Populate.Publisher import __main__ as populate_publisher
from Populate.Author import __main__ as populate_author
from Populate.Genre import __main__ as populate_genre
from time import sleep
import sys
sys.path.append("./sprint2_populating_Alt/Populate")

from sprint2_populating_Alt.Populate.User import __main__ as populate_user
from sprint2_populating_Alt.Populate.BookSource import __main__ as populate_book_source
from sprint2_populating_Alt.Populate.Mean import __main__ as populate_mean
from sprint2_populating_Alt.Populate.Media import __main__ as populate_media

from sprint2_populating_Alt.Populate.Book.Book import __main__ as new_populate_book
from sprint2_populating_Alt.Populate.Book.book_cover import __main__ as populate_book_cover
from sprint2_populating_Alt.Populate.Book.Genre import __main__ as new_populate_genre
from sprint2_populating_Alt.Populate.Book.Publisher import __main__ as new_populate_publisher
from sprint2_populating_Alt.likes_book import __main__ as populate_like_book

def __main__():
    """
    This function is the main function of the application. It calls the main functions of all the modules to populate the database.

    Returns:
        bool: True if the database is populated successfully, False otherwise.

    Raises:
        Exception: If an error occurs while populating the database.
    """
    '''try:
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
        return False'''
    try:
        populate_book_cover()
    except Exception as e:
        print(f"Error while populating the database: {e}")
        return False

    return True

if __name__ == '__main__':
    __main__()