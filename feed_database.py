import csv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.Repository_leaderboard import LeaderBoard_Repository

engine = create_engine("sqlite:///leaderboard.db", pool_pre_ping=True)
# create the table
declarative_base().metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def feed_database(data_path):
    # open the CSV file
    with open(data_path, newline='') as csvfile:
        # create a CSV reader object
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # iterate over each row in the file
        next(reader, None)
        for row in reader:
            # create a new leaderboard entry
            add_leaderboard = LeaderBoard_Repository(session)
            add_leaderboard.create_Leaderboard(row[0], "ramses", row[1])

    session.close()
    
feed_database("pipeline_result.csv")
    
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import data from a CSV file into a database.')
    parser.add_argument('db_uri', help='URI of the database')
    parser.add_argument('csv_path', help='Path to the CSV file')
    args = parser.parse_args()

    main(args.db_uri, args.csv_path)

import streamlit as st
import pandas as pd
import base64

# Fonction pour télécharger un fichier CSV
def download_csv(df, file_name):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Télécharger {file_name}</a>'
    return href

# Chargement des fichiers CSV
data1 = pd.read_csv('')
data2 = pd.read_csv('C:/Users/sylva/OneDrive/Bureau/API_Docker_Hetic_2023/Docker_Api_Tp_Final/TP_AWS_SYLOU/samples/users.csv')

# Affichage des tableaux
st.write("Tableau 1 :")
st.write(data1)

st.write("Tableau 2 :")
st.write(data2)

# Bouton de téléchargement
if st.button('Télécharger les données'):
    st.markdown(download_csv(data1, 'message.csv'), unsafe_allow_html=True)
    st.markdown(download_csv(data2, 'user.csv'), unsafe_allow_html=True)
"""
