import utils.SQL_controleur.SQL_controleur as sql

def test():

    script = 'Select * from book'
    # Créer la base de données
    res = sql.requete(script, no_limit = True)

    return res

res = test()

print(res)