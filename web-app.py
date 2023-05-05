import streamlit as st
import pandas as pd
import subprocess
import os


# Titre de l'application
st.markdown("<h1 style='color:blue;'> APPLICATION STREAMLIT</h1>", unsafe_allow_html=True)

# Créer un menu à gauche
menu = ["Accueil", "Aggregation", "Feed Pipeline"]
choix = st.sidebar.selectbox("Barre de Navigation", menu)

# Afficher la page d'accueil
if choix == "Accueil":
    st.write("<h2 style='color:red;'>Bienvenue sur l'application Streamlit</h2>", unsafe_allow_html=True)

# Afficher le formulaire d'upload et le bouton d'aggregation
if choix == "Aggregation":
    st.write("### <h1 style='color:red;'>Télécharger les fichiers </h1>", unsafe_allow_html=True)
    file1 = st.file_uploader("messages.csv")
    file2 = st.file_uploader("users.csv")
    
    if st.button('Aggregation'):
        # Vérifier si les fichiers ont été uploadés
        if file1 and file2:
            # Charger les fichiers CSV dans des dataframes pandas
            df_messages = pd.read_csv(file1)
            df_users = pd.read_csv(file2)

            # Renommer la colonne 'first_name' en 'name' dans le dataframe df_users
            df_users = df_users.rename(columns={'first_name': 'name'})

            # Renommer la colonne 'author_id' en 'user_id' dans le dataframe df_messages
            df_messages = df_messages.rename(columns={'author_id': 'user_id'})
            
            # Renommer la colonne 'content' en 'message' dans le dataframe df_messages
            df_messages = df_messages.rename(columns={'content': 'message'})

            # Fusionner les deux dataframes
            df_concat = pd.merge(df_messages, df_users, on='user_id', how='left')

            # Sélectionner les colonnes 'user_id', 'name' et 'content'
            df_concat = df_concat[['user_id', 'name', 'message']]

            # Enregistrer le résultat dans un fichier CSV nommé pipeline_result.csv
            df_concat.to_csv("../pipeline_result.csv", index=False)

            # Afficher le contenu du fichier pipeline_result.csv
            st.write("Contenu du fichier pipeline_result.csv :")
            st.write(df_concat)
        else:
            st.write("Veuillez uploader deux fichiers pour continuer.")

# Ouvrir le fichier feed-pipeline.py
if choix == "Feed Pipeline":
    st.write("<h4 style='color:green;'>Cliquez pour ouvrir Feed Pipeline</h4>", unsafe_allow_html=True)
    if st.button("Feed Pipeline"):
        subprocess.Popen(["streamlit", "run", "feed-pipeline.py"])