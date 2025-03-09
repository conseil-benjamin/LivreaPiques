import os
import time
import sprint2_populating.application.populate as ppl
import test

def populateDatabase():
    if os.getenv('POPULATE_DB', 'false').lower() == 'true':
        print("Populating the database...")
        if ppl.populate():
            print("Database populated successfully.")
        else:
            print("Database population failed")
    else:
        print("Skipping database population.")

def __main__():
    populateDatabase()
    print("Application is running")
    test.test()
    while True:
        time.sleep(60)

if __name__ == "__main__":
    __main__()