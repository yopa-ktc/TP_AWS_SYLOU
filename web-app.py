import streamlit as st
import pandas as pd

# Titre de l'application
st.markdown("<h1 style='color:blue;'>Mon application Streamlit</h1>", unsafe_allow_html=True)

# Définir les champs d'upload de fichiers
st.write("### <h1 style='color:red;'>Télécharger les fichiers </h1>", unsafe_allow_html=True)
file1 = st.file_uploader("messages.csv")
file2 = st.file_uploader("users.csv")

# Créer le bouton pour afficher les chemins des fichiers uploadés
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

        # Fusionner les deux dataframes
        df_concat = pd.merge(df_messages, df_users, on='user_id', how='left')

        # Sélectionner les colonnes 'user_id', 'name' et 'content'
        df_concat = df_concat[['user_id', 'name', 'content']]

        # Enregistrer le résultat dans un fichier CSV nommé pipeline_result.csv
        df_concat.to_csv("pipeline_result.csv", index=False)

        # Afficher le contenu du fichier pipeline_result.csv
        st.write("Contenu du fichier pipeline_result.csv :")
        st.write(df_concat)
    else:
        st.write("Veuillez uploader deux fichiers pour continuer.")
