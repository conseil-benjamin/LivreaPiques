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

# Changez les permissions des fichiers dans le répertoire new_data
chmod -R 777 ./new_data

# Exécutez docker-compose up avec la variable d'environnement
POPULATE_DB=$POPULATE_DB docker compose down
POPULATE_DB=$POPULATE_DB docker compose build
POPULATE_DB=$POPULATE_DB docker compose up