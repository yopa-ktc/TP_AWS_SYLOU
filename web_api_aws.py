import csv
import io
import streamlit as st
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Repository_leaderboard import LeaderBoard_Repository
from sqlalchemy.ext.declarative import declarative_base


API_URL = "http://127.0.0.1:5000/feed"

# Configuration de l'accès à la base de données
DB_NAME = 'leaderboard.db'  # Remplacez par le nom de votre fichier de base de données SQLite

# Configuration de l'accès à AWS S3
AWS_ACCESS_KEY_ID = 'AKIA2BHJHJTWXQQZBRUC'
AWS_SECRET_ACCESS_KEY = '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'
S3_LEADERBOARD_BUCKET = 'pipeline-aggre-result-data-bucket-md4-api'
S3_FILE_NAME = 'pipeline_result.csv'

# Création du moteur SQLAlchemy
db_url = f"sqlite:///{DB_NAME}"
engine = create_engine(db_url, pool_pre_ping=True)

declarative_base().metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Création de la session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

def fetch_csv_from_s3():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # Téléchargement du fichier CSV depuis S3
    response = s3_client.get_object(Bucket=S3_LEADERBOARD_BUCKET, Key=S3_FILE_NAME)
    content = response['Body'].read().decode('utf-8')

    # Lecture du contenu CSV
    csv_data = csv.reader(io.StringIO(content))

    # Retourner les données CSV
    return csv_data

def insert_data_to_database(csv_file_path):
    # open the CSV file
    with open(csv_file_path, newline='') as csvfile:
        # create a CSV reader object
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # iterate over each row in the file
        next(reader, None)
        for row in reader:
            # create a new leaderboard entry
            add_leaderboard = LeaderBoard_Repository(session)
            add_leaderboard.create_Leaderboard(row[0], row[1], row[2])
            
    # Commit des changements dans la base de données
    session.commit()
    session.close()



def main():
    st.title("Alimenter la base de données")

    # Bouton pour récupérer les données depuis S3 et les afficher
    if st.button("Afficher le fichier CSV"):
        csv_data = fetch_csv_from_s3()
        st.table(csv_data)

    # Bouton pour récupérer les données depuis S3 et les insérer dans la base de données
    if st.button("Alimenter la base de données"):
        csv_file_path = "pipeline_result.csv"  # Chemin du fichier CSV téléchargé depuis S3
        insert_data_to_database(csv_file_path)
        st.success("Les données ont été ajoutées à la base de données avec succès!")


if __name__ == "__main__":
    main()
