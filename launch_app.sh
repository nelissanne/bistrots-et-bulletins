#!/bin/bash
# Installe les dépendances et lance l'application Shiny

python -m pip install -r requirements.txt
export QUARTO_PYTHON="$(which python)"
quarto serve analyse/interactive.qmd --port 5000 --host 0.0.0.0

#https://user-<username>-190909-0.user.lab.sspcloud.fr/proxy/5000/