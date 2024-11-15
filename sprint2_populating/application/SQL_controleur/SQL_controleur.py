import pandas as pd
from sqlalchemy import create_engine, select, Table, MetaData
from sqlalchemy.orm import sessionmaker
import yaml
import time
from tqdm import tqdm

# Import la donnée du fichier yml
with open('sprint2_populating/application/config.yml', 'r') as file:
    config = yaml.safe_load(file)


def conexion_db():
    try:
        ## URL of the database
        database_url = config['adress_sql']
        engine = create_engine(database_url)
        session = sessionmaker(bind=engine)
        session = session()
        print("Connection to the database successful")
        return engine, session
    except:
        raise Exception("Error in the connection to the database")

def insert(dataframe, table_name):
    attempts = 3
    interval = 3
    for attempt in range(attempts):
        try:
            engine = conexion_db()[0]
            break
        except Exception as e:
            if attempt < attempts - 1:
                time.sleep(interval)
            else:
                raise Exception("Failed to connect to the database after multiple attempts") from e
    try:
        dataframe.to_sql(table_name, con=engine, if_exists='append', index=False)
        print("Data inserted into the database")
        return True
    except Exception as e:
        print(f"Error inserting data into the database : {e}")
        return False
    
def insert_table_assocation(dataframe, table1, table2, table1_key, table2_key, table1_id, table2_id):
    attempts = 3
    interval = 3
    for attempt in range(attempts):
        try:
            engine = conexion_db()[0]
            session = conexion_db()[1]
            break
        except Exception as e:
            if attempt < attempts - 1:
                time.sleep(interval)
            else:
                raise Exception("Failed to connect to the database after multiple attempts") from e

    try:
        # Load the tables with the engine
        table1 = Table(table1, MetaData(), autoload_with=engine)
        table2 = Table(table2, MetaData(), autoload_with=engine)
    except Exception as e:
        raise Exception("Error loading tables with the engine") from e

    try:
        # Get all the values of the table
        exec1 = select(table1.c[table1_id], table1.c[table1_key])
        exec2 = select(table2.c[table2_id], table2.c[table2_key])

        print(exec1)
        print(exec2)
        table1_record = session.execute(select(table1.c[table1_id], table1.c[table1_key])).fetchall()
        table2_record = session.execute(select(table2.c[table2_id], table2.c[table2_key])).fetchall()
    except Exception as e:
        print(e)
        raise Exception("Error fetching records from tables") from e

    try:
        # Create a dictionary with the values of the table
        table1_dict = {table1_key: table1_id for table1_id, table1_key in table1_record}
        table2_dict = {table2_key: table2_id for table2_id, table2_key in table2_record}
    except Exception as e:
        raise Exception("Error creating dictionaries from table records") from e

    try:
        # Create the associations using the dictionaries, with a progress bar
        associations = []
        for index, row in tqdm(dataframe.iterrows(), total=len(dataframe), desc='Creating associations'):
            print(f"row: {row}")
            table1_id_base = table1_dict.get(row[f'{table1_key}'])
            print(f"table1_id: {table1_id}")
            table2_id_base = table2_dict.get(row[f'{table2_key}'])
            print(f"table2_id: {table2_id}")
            # Check that both IDs exist before inserting
            if table1_id_base is not None and table2_id_base is not None:
                print("coucou")
                associations.append({table1_id: table1_id_base, table2_id: table2_id_base})
                print(f"Association created between {table1_id_base} and {table1_id_base}")
            else:
                print(f"Association NOT created between {table1_id_base} and {table2_id_base}")
    except Exception as e:
        print(e)
        print(f"coucou{e}")
        raise Exception("Error creating associations") from e

    try:
        # Save the associations to the CSV file
        associations_df = pd.DataFrame(associations)
        associations_df.to_csv('new_data/Associations{table1}_{table2}.csv'.format(table1=table1, table2=table2), index=False)
    except Exception as e:
        raise Exception("Error saving associations to CSV file") from e

    try:
        associations_df = associations_df.drop_duplicates()
        associations_df.to_sql(f"{table1}_{table2}", con=engine, if_exists='append', index=False)
        return True
    except Exception as e:
        raise Exception("Error inserting associations into the database") from e
    
