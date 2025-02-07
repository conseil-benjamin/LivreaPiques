from SQL_controleur.SQL_controleur import *
from system_reco.reco_esteban import *
from system_reco.reco_benjamin import *
from system_reco.reco_pierig_remake import main as recommend_books
from system_reco.reco_description import *


def main():
    #demander si on veut la 1er reco
    user_id = int(input("Entrez l'id de l'utilisateur: "))
    if input("Voulez-vous la première recommandation ? (Y/N)") == "Y":
        print(reco_esteban(user_id))

    if input("Voulez-vous la deuxième recommandation ? (Y/N)") == "Y":
        reco_benj = FinalRecommender()
        print(reco_benj.get_recommendations(1, 5))

    if input("Voulez-vous la troisième recommandation ? (Y/N)") == "Y":
        print(recommend_books(user_id))
    
    if input("Voulez-vous la quatrième recommandation ? (Y/N)") == "Y":
        print(reco_description(user_id))

if __name__ == '__main__':
    main()