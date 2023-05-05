import csv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.Repository_leaderboard import LeaderBoard_Repository
import io

engine = create_engine("sqlite:///leaderboard.db", pool_pre_ping=True)
# create the table
declarative_base().metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def feed_database(data_path):
    # lire le contenu du fichier CSV
    content = data_path.read()

    # créer un flux en mémoire à partir des données lues
    stream = io.BytesIO(content)

    # créer un lecteur CSV à partir du flux
    reader = csv.reader(io.TextIOWrapper(stream, newline=''))

    # itérer sur les lignes du CSV
    next(reader, None)
    for row in reader:
        # créer une nouvelle entrée dans la table leaderboard
        add_leaderboard = LeaderBoard_Repository(session)
        add_leaderboard.create_Leaderboard(row[0], row[1], row[2])

    session.close()


import requests
import streamlit as st

API_URL = "http://127.0.0.1:5000/feed"

def main():
    st.title("Feed Pipeline")

    # Formulaire pour sélectionner le fichier CSV
    data_path = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    # Bouton pour envoyer la requête POST
    if st.button("Alimenter la base de données"):
        if data_path is None:
            st.warning("Veuillez sélectionner un fichier")
        elif data_path.name != "pipeline_result.csv":
            st.error("Nom du fichier incorrect")
        else:
            feed_database(data_path)
            st.success("Les données ont été ajoutées à la base de données avec succès!")

if __name__ == "__main__":
    main()
