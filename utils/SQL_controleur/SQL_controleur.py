import pandas as pd
from sqlalchemy import create_engine, select, Table, MetaData, text
from sqlalchemy.orm import sessionmaker
import yaml
import time
from tqdm import tqdm

# Import la donnée du fichier yml
try:
    with open('utils/config.yml', 'r') as file:
        config = yaml.safe_load(file)
except Exception as e:
    raise Exception(f"Error loading the configuration file : {e}") from e


def conexion_db():
    """
    Establishes a connection to t-10he SQL database.
    
    Returns:
        tuple: (engine, session) where:
            - engine: The SQLAlchemy Engine object connected to the database.
            - session: A SQLAlchemy session for executing queries.
    
    Raises:
        Exception: If the connection to the database fails.
    """
    try:
        ## URL of the database
        database_url = config['adress_sql']
        schema = config['schema']
        engine = create_engine(database_url)
        session = sessionmaker(bind=engine)
        session = session()
        return engine, session, schema
    except Exception as e:
        raise Exception(f"Error in the connection to the database : {e}") from e
    

def set_search_path(engine, schema):
    """
    Sets the search path for the database session to the specified schema.
    
    Args:
        engine: The SQLAlchemy engine object.
        schema (str): The schema to set as the search path.
    """
    with engine.connect() as connection:
        connection.execute(text(f"SET search_path TO {schema}"))

def requete(requete, no_limit=False, no_schema=False):
    """
    Execute a query on the database., if the number of rows is greater than 1000, the function will make several requests

    Args:
        requete (str): The query to execute.

    Returns:
        pd.DataFrame: The result of the query.
    """
    try:
        print("Connection to the database successful")
        engine, session, schema = conexion_db()
        if not no_schema:
            set_search_path(engine, schema)
    except Exception as e:
        raise Exception(f"Failed to connect to the database : {e}") from e
    
    try:
        # Execute the query
        if no_limit:
            result = pd.read_sql(requete, engine)
        else:
            chunk = 0
            requete_with_limit = requete + f" LIMIT 2000 OFFSET {chunk};"
            result = pd.read_sql(requete_with_limit, engine)
            while len(result) - chunk >= 2000:
                chunk = chunk + 2000
                requete_with_limit = requete + f" LIMIT 2000 OFFSET {chunk};"
                print(requete_with_limit)
                result = pd.concat([result, pd.read_sql(requete_with_limit, engine)])
    except Exception as e:
        raise Exception(f"Error executing query : {e}") from e
    return result

def create_database():
    print("Creating the database...")
    # Récupérer les scripts de création de la base de données	
    with open('sprint2_create_database/database.sql', 'r') as file:
        script = file.read()
        
    try:
        print("Connecting to the database...")
        engine, session, schema = conexion_db()
        print("Connection to the database successful")
    except Exception as e:
        raise Exception(f"Failed to connect to the database : {e}") from e
    
    try:
        session.execute(text(script))
        session.commit()
        print("Database created successfully")
        return True
    except Exception as e:
        print(f"Error creating the database: {e}")
        return False

def insert(dataframe, table_name):
    """
    Inserts data from a pandas DataFrame into a SQL table.
    
    Args:
        dataframe (pd.DataFrame): The DataFrame containing data to insert.
        table_name (str): The name of the target table in the database.
    
    Returns:
        bool: True if the data is inserted successfully, False otherwise.
    
    Raises:
        Exception: If connection fails after multiple attempts.
    """
    attempts = 3
    interval = 3
    for attempt in range(attempts):
        try:
            engine, session, schema = conexion_db()
            print("Connection to the database successful")
            break
        except Exception as e:
            if attempt < attempts - 1:
                time.sleep(interval)
            else:
                raise Exception(f"Failed to connect to the database after multiple attempts: {e}") from e
    try:
        print("Inserting data into " + table_name)
        dataframe.to_sql(table_name, con=engine, if_exists='append', index=False)
        print("Data inserted into the database")
        return True
    except Exception as e:
        print(f"Error inserting data into the database : {e}")
        return False
    
def insert_table_assocation(dataframe, table1, table2, table1_key, table2_key, table1_id, table2_id, table_name=None):
    """
    Creates and inserts associations between two SQL tables.
    
    Args:
        dataframe (pd.DataFrame): The DataFrame containing data to create associations.
        table1 (str): Name of the first table in the database.
        table2 (str): Name of the second table in the database.
        table1_key (str): Name of the secondary key used to identify records in `table1`.
        table2_key (str): Name of the secondary key used to identify records in `table2`.
        table1_id (str): Name of the column containing the ID in `table1`.
        table2_id (str): Name of the column containing the ID in `table2`.
        table_name (str) (optionnal): Name given to the created associations table.
    
    Returns:
        bool: True if the associations are successfully inserted.
    
    Raises:
        Exception: If any step in the process fails (connection, data retrieval, etc.).
    """
    attempts = 3
    interval = 3
    for attempt in range(attempts):
        try:
            engine, session, schema = conexion_db()
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
        print(e)
        raise Exception("Error loading tables with the engine") from e

    try:
        # Get all the values of the table
        exec1 = select(table1.c[table1_id], table1.c[table1_key])
        exec2 = select(table2.c[table2_id], table2.c[table2_key])

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
            table1_id_base = table1_dict.get(row[f'{table1_key}'])
            table2_id_base = table2_dict.get(row[f'{table2_key}'])
            # Check that both IDs exist before inserting
            if table1_id_base is not None and table2_id_base is not None:
                associations.append({table1_id: table1_id_base, table2_id: table2_id_base})
                #print(f"Association created between {table1_id_base} and {table2_id_base}")
            #else:
            #    print(f"Association NOT created between {table1_id_base} and {table2_id_base}")
    except Exception as e:
        print(e)
        raise Exception("Error creating associations") from e

    try:
        # Save the associations to the CSV file
        associations_df = pd.DataFrame(associations)
        if (table_name is not None):
            associations_df.to_csv(f'new_data/Associations_{table_name}.csv', index=False)
        else:
            associations_df.to_csv('new_data/Associations_{table1}_{table2}.csv'.format(table1=table1, table2=table2), index=False)
    except Exception as e:
        raise Exception("Error saving associations to CSV file", e) from e

    try:
        associations_df = associations_df.drop_duplicates()
        if (table_name is not None):
            associations_df.to_sql(f"{table_name}", con=engine, if_exists='append', index=False)
        else:
            associations_df.to_sql(f"{table1}_{table2}", con=engine, if_exists='append', index=False)
        return True
    except Exception as e:
        raise Exception("Error inserting associations into the database") from e
    
def insert_table_assocation_book(dataframe, table1, table1_key, table1_id):
    """
    Creates and inserts associations between an SQL table and the book table.
    
    Args:
        dataframe (pd.DataFrame): The DataFrame containing data to create associations.
        table1 (str): Name of the first table in the database.
        table1_key (str): Name of the secondary key used to identify records in `table1`.
        table1_id (str): Name of the column containing the ID in `table1`.
    
    Returns:
        bool: True if the associations are successfully inserted.
    
    Raises:
        Exception: If any step in the process fails (connection, data retrieval, etc.).
    """
    attempts = 3
    interval = 3
    for attempt in range(attempts):
        try:
            engine, session, schema = conexion_db()
            break
        except Exception as e:
            if attempt < attempts - 1:
                time.sleep(interval)
            else:
                raise Exception("Failed to connect to the database after multiple attempts") from e

    try:
        # Load the tables with the engine
        table1 = Table(table1, MetaData(), autoload_with=engine)
        book = Table('book', MetaData(), autoload_with=engine)
    except Exception as e:
        print(e)
        raise Exception("Error loading tables with the engine") from e

    # la table livre n'as pas de clé secondaire mais on a l'id du livre donc on a pas besoin de la recuperer
    try:
        # Get all the values of the table
        exec1 = select(table1.c[table1_id], table1.c[table1_key])

        table1_record = session.execute(select(table1.c[table1_id], table1.c[table1_key])).fetchall()
    except Exception as e:
        print(e)
        raise Exception("Error fetching records from tables") from e
    
    try:
        # Create a dictionary with the values of the table
        table1_dict = {table1_key: table1_id for table1_id, table1_key in table1_record}
    except Exception as e:
        raise Exception("Error creating dictionaries from table records") from e
    
    try:
        # Create the associations using the dictionaries, with a progress bar
        associations = []
        for index, row in tqdm(dataframe.iterrows(), total=len(dataframe), desc='Creating associations'):
            table1_id_base = table1_dict.get(row[f'{table1_key}'])
            # Check that both IDs exist before inserting
            if table1_id_base is not None:
                associations.append({table1_id: table1_id_base, 'book_id': row['book_id']})
                #print(f"Association created between {table1_id_base} and {row['book_id']}")
            #else:
            #    print(f"Association NOT created between {table1_id_base} and {row['book_id']}")
    except Exception as e:
        print(e)
        print(f"coucou{e}")
        raise Exception("Error creating associations") from e
    
    try:
        # Save the associations to the CSV file
        associations_df = pd.DataFrame(associations)
        associations_df.to_csv('new_data/Associations{table1}_book.csv'.format(table1=table1), index=False)
    except Exception as e:
        raise Exception("Error saving associations to CSV file", e) from e
    
    try:
        associations_df = associations_df.drop_duplicates()
        associations_df.to_sql(f"book_{table1}", con=engine, if_exists='append', index=False)
        return True
    except Exception as e:
        raise Exception("Error inserting associations into the database") from e
    
