#!/bin/bash

# Par défaut, ne pas peupler la base de données
POPULATE_DB=false
WITHOUT_DB=false
BUILD=false

# Vérifiez les arguments de ligne de commande

while getopts "pdb" opt; do
  case ${opt} in
    p )
      POPULATE_DB=true
      ;;
    d )
      WITHOUT_DB=true
      ;;
    b )
      BUILD=true
      ;; 
    \? )
      echo "Usage: cmd [-p] [-d] [-b]"
      exit 1
      ;;
  esac
done

# Créez le dossier caches avec les droits dans le dossier application_system_reco
mkdir -p ./application_system_reco/caches
chmod 777 ./application_system_reco/caches

# Exécutez docker-compose up avec la variable d'environnement
docker compose down
if [ "$BUILD" = true ]; then
  docker compose build
fi

if [ "$WITHOUT_DB" = true ]; then
  POPULATE_DB=$POPULATE_DB docker compose up app react-app
else
  POPULATE_DB=$POPULATE_DB docker compose up
fi
