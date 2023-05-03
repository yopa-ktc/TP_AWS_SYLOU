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
            st.error("Chemin du fichier non identifié")
        else:
            response = requests.post(API_URL, json={"data_path": data_path.name})

            if response.ok:
                message = response.json()["message"]
                st.success(message)
            else:
                st.error("Erreur lors de la requête")
                
                
        # Bouton pour ouvrir l'interface web-api.py


if __name__ == "__main__":
    main()
