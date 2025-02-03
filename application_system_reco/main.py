from SQL_controleur.SQL_controleur import *
from system_reco.reco_esteban import *
from system_reco.reco_benjamin import *

def main():
    print(reco_esteban(1))
    reco_benj = FinalRecommender()
    print(reco_benj.get_recommendations(1, 5))

if __name__ == '__main__':
    main()
