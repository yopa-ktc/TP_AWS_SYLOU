import pandas as pd
import streamlit as st


# Charger les données
data1 = pd.read_csv('C:/Users/sylva/OneDrive/Bureau/API_Docker_Hetic_2023/Docker_Api_Tp_Final/TP_AWS_SYLOU/samples/messages.csv')
data2 = pd.read_csv('C:/Users/sylva/OneDrive/Bureau/API_Docker_Hetic_2023/Docker_Api_Tp_Final/TP_AWS_SYLOU/samples/users.csv')

# Renommer la colonne 'author_id' pour pouvoir fusionner les dataframes
data1 = data1.rename(columns={'author_id': 'user_id'})

# Fusionner les données
pipeline_result = pd.merge(data1, data2, on='user_id')

# Créer une liste des identifiants d'utilisateurs uniques
unique_users = pipeline_result['user_id'].unique()
unique_users2 = pipeline_result['first_name'].unique()

# Fonction de formatage pour afficher le first_name sans parenthèses
def format_func(user_id):
    first_name = unique_users2[unique_users==user_id][0]
    return first_name

# Sélectionner l'utilisateur à afficher
selected_user = st.selectbox('Sélectionner un utilisateur', unique_users)

# Récupérer le first_name et le content correspondant à l'utilisateur sélectionné
selected_first_name = pipeline_result.loc[pipeline_result['user_id']==selected_user, 'first_name'].iloc[0]
selected_content = pipeline_result.loc[pipeline_result['user_id']==selected_user, 'content'].tolist()

# Afficher le first_name et le content correspondant à l'utilisateur sélectionné
st.write(f"Prénom: {selected_first_name}")

st.write("Messages de l'utilisateur sélectionné :")
for message in selected_content:
    st.write('- ' + message)

    
# # Sauvegarder le dataframe au format CSV  
# pipeline_result[['user_id', 'first_name', 'content']].to_csv('pipeline_result1.csv', index=False)
