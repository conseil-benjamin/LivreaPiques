import os
import uvicorn

import sprint2_populating.application.populate as ppl

def populate_database():
    print(os.getenv('POPULATE_DB', 'false'))
    if os.getenv('POPULATE_DB', 'false').lower() == 'true':
        print("Populating the database...")
        if ppl.populate():
            print("Database populated successfully.")
        else:
            print("Database population failed")
    else:
        print("Skipping database population.")

def startAPI():
    uvicorn.run("application_system_reco.api:app", host="0.0.0.0", port=8000, reload=True)


def __main__():
    populate_database()
    print("Application is running")
    startAPI()

if __name__ == "__main__":
    __main__()