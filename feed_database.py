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
