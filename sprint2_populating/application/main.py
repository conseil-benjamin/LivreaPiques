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

from User import __main__ as populate_user
from BookSource import __main__ as populate_book_source
from Mean import __main__ as populate_mean
from Media import __main__ as populate_media
from liked_genre import __main__ as populate_liked_genre


def __main__():
    """
    This function is the main function of the application. It calls the main functions of all the modules to populate the database.

    Returns:
        bool: True if the database is populated successfully, False otherwise.

    Raises:
        Exception: If an error occurs while populating the database.
    """
    try:
        print('populate_liked_genre')
        populate_liked_genre()
    except Exception as e:
        print(f"Error while populating the database: {e}")
        return False
    
    return True

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
        populate_liked_genre()
    except Exception as e:
        print(f"Error while populating the database: {e}")
        return False
    

    return True

if __name__ == '__main__':
    __main__()