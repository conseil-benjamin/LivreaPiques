#!/bin/bash

# Par défaut, ne pas peupler la base de données
POPULATE_DB=false

# Vérifiez les arguments de ligne de commande
while getopts "p" opt; do
  case ${opt} in
    p )
      POPULATE_DB=true
      ;;
    \? )
      echo "Usage: cmd [-p]"
      exit 1
      ;;
  esac
done

# Créez le dossier caches avec les droits dans le dossier application_system_reco
<<<<<<< HEAD
mkdir -p ./application_system_reco/caches
chmod 777 ./application_system_reco/caches

# Exécutez docker-compose up avec la variable d'environnement
POPULATE_DB=$POPULATE_DB docker compose down
#POPULATE_DB=$POPULATE_DB docker compose build
POPULATE_DB=$POPULATE_DB docker compose up
=======
mkdir -p application_system_reco/caches
chmod 777 application_system_reco/caches


# Exécutez docker-compose up avec la variable d'environnement
POPULATE_DB=$POPULATE_DB docker compose down
POPULATE_DB=$POPULATE_DB docker compose build
POPULATE_DB=$POPULATE_DB docker compose up
>>>>>>> 0a92c8ab4878c9e22e4205411005405b3aed118a
