import pandas as pd
import streamlit as st


# Charger les données
data1 = pd.read_csv('./samples/messages.csv')
data2 = pd.read_csv('./samples/users.csv')

# Renommer la colonne 'author_id' pour pouvoir fusionner les dataframes
data1 = data1.rename(columns={'author_id': 'user_id'})

# Fusionner les données
pipeline_result = pd.merge(data1, data2, on='user_id')

# Créer une liste des identifiants d'utilisateurs uniques
unique_users = pipeline_result['user_id'].unique()

# Sélectionner l'utilisateur à afficher
selected_user = st.selectbox('Sélectionner un utilisateur', unique_users)

# Filtrer les messages de l'utilisateur sélectionné
user_messages = pipeline_result[pipeline_result['user_id'] == selected_user]['content']

# Afficher les messages
st.write('Messages de l\'utilisateur sélectionné :')
for message in user_messages:
    st.write('- ' + message)
    
# Sauvegarder le dataframe au format CSV
pipeline_result[['user_id', 'content']].to_csv('pipeline_result.csv', index=False)