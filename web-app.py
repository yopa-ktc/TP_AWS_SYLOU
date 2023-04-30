import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Mon application Streamlit")

# Création des onglets
menu = ["Telechargement", "Classement"]
choice = st.sidebar.selectbox("Choisir une option", menu)

# Si l'utilisateur a choisi l'onglet "Telechargement"
if choice == "Telechargement":
    st.subheader("Téléchargement des fichiers CSV")
    
    # Téléchargement de messages.csv
    st.write("### Téléchargement de messages.csv")
    df_messages = pd.read_csv("C:/Users/sylva/OneDrive/Bureau/API_Docker_Hetic_2023/Docker_Api_Tp_Final/TP_AWS_SYLOU/samples/messages.csv")
    st.success("Le fichier messages.csv a été bien enregistré")
    # Créer un bouton de téléchargement pour le fichier messages.csv
    st.download_button(
        label="Télécharger messages.csv",
        data=df_messages.to_csv().encode("utf-8"),
        file_name="messages.csv",
        mime="text/csv"
    )
    
    # Téléchargement de users.csv
    st.write("### Téléchargement de users.csv")
    df_users = pd.read_csv("C:/Users/sylva/OneDrive/Bureau/API_Docker_Hetic_2023/Docker_Api_Tp_Final/TP_AWS_SYLOU/samples/users.csv")
    st.success("Le fichier users.csv a été bien enregistré")
    # Créer un bouton de téléchargement pour le fichier users.csv
    st.download_button(
        label="Télécharger users.csv",
        data=df_users.to_csv().encode("utf-8"),
        file_name="users.csv",
        mime="text/csv"
    )

# Si l'utilisateur a choisi l'onglet "Classement"
elif choice == "Classement":
    st.subheader("Affichage du fichier results.csv")
    
    # Chargement du fichier results.csv
    try:
        df_results = pd.read_csv("results.csv")
        st.write(df_results)
    except FileNotFoundError:
        st.warning("Le fichier results.csv n'a pas été trouvé dans le dossier Streamlit")
