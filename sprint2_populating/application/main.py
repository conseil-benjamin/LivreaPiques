from Populate.Book import __main__ as populate_book
from Populate.Character import __main__ as populate_character
from Populate.Series import __main__ as populate_series
from Populate.Award import __main__ as populate_award
from Populate.Publisher import __main__ as populate_publisher
from Populate.Author import __main__ as populate_author
from Populate.Genre import __main__ as populate_genre
from time import sleep

def __main__():
    """
    This function is the main function of the application. It calls the main functions of all the modules to populate the database.

    Returns:
        bool: True if the database is populated successfully, False otherwise.

    Raises:
        Exception: If an error occurs while populating the database.
    """

    
    try:
        # populate_book()
        sleep(1)
    except Exception as e:
        print(f"Error while populating the database: {e}")
        return False
    
    try:
        populate_character()
        sleep(1)
    except Exception as e:
        print(f"Error while populating the database: {e}")
        return False

    try:
        # populate_series()
        sleep(1)
    except Exception as e:
        print(f"Error while populating the database: {e}")
        return False
    
    try:
        # populate_award()
        sleep(1)
    except Exception as e:
        print(f"Error while populating the database: {e}")
        return False
    
    try:
        # populate_publisher()
        sleep(1)
    except Exception as e:
        print(f"Error while populating the database: {e}")
        return False
    
    try:
        # populate_author()
        sleep(1)
    except Exception as e:
        print(f"Error while populating the database: {e}")
        return False
    try:
        # populate_genre()
        sleep(1)
    except Exception as e:
        print(f"Error while populating the database: {e}")
        return False
    
    return True


if __name__ == '__main__':
    __main__()
