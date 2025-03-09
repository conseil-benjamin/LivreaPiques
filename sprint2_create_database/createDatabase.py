from utils.SQL_controleur.SQL_controleur import requete


def createDatabase():

    # Récupérer les scripts de création de la base de données	
    with open('sprint2_create_database/database.sql', 'r') as file:
        script = file.read()
        
    # Créer la base de données
    requete(script, no_limit = True, no_schema=True)
    