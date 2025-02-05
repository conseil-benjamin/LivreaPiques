from SQL_controleur.SQL_controleur import *
from system_reco.reco_esteban import *
from system_reco.reco_benjamin import *
from system_reco.reco_pierig import *
from system_reco.reco_description import *

def main():
    '''Ce programme à pour but de comparer les 4 systèmes de recommandation de livre en fonction du temps de calcul
    pour cela on fait n fois chaque recommandation et on calcule le temps moyen'''
    n = 10
    user_id = 69
    time_esteban = 0
    time_benjamin = 0
    time_pierig = 0
    time_description = 0

    for i in range(n):
        print('-'*100)
        print('reco esteban')
        start = time.time()
        print(reco_esteban(user_id, 5))
        time_esteban += time.time() - start

        print('-'*100)
        print('reco benjamin')
        start = time.time()
        reco_benj = FinalRecommender()
        print(reco_benj.get_recommendations(1, 5))
        time_benjamin += time.time() - start

        #start = time.time()
        #print(recommend_books(user_id))
        #time_pierig += time.time() - start

        print('-'*100)
        print('reco description')
        start = time.time()
        print(reco_description(user_id, 5, True, True, False))
        time_description += time.time() - start
    
    print(f"temps moyen pour la reco esteban : {time_esteban/n}")
    print(f"temps moyen pour la reco benjamin : {time_benjamin/n}")
    print(f"temps moyen pour la reco pierig : {time_pierig/n}")
    print(f"temps moyen pour la reco description : {time_description/n}")

if __name__ == '__main__':
    main()
    
