import streamlit as st
import boto3
import pandas as pd
from io import StringIO


# Connexion au service S3
s3 = boto3.resource('s3')

# Fonction pour récupérer les fichiers CSV
def get_csv_files():
    # Nom du bucket source et des fichiers CSV
    source_bucket_name = 'sylvaind-raw-data-bucket-md4-api'
    users_file_name = 'users.csv'
    messages_file_name = 'messages.csv'
    
    # Télécharger les fichiers CSV depuis le bucket source
    users_file_object = s3.Object(source_bucket_name, users_file_name).get()['Body'].read().decode('utf-8')
    messages_file_object = s3.Object(source_bucket_name, messages_file_name).get()['Body'].read().decode('utf-8')

    # Convertir les fichiers CSV en DataFrames pandas
    users_df = pd.read_csv(StringIO(users_file_object))
    messages_df = pd.read_csv(StringIO(messages_file_object))
    
    # Renommer la colonne 'content' en 'message' et 'author_id' en 'user_id'
    aggregated_df = aggregated_df.rename(columns={'content': 'message'})
    aggregated_df = aggregated_df.rename(columns={'author_id': 'user_id'})
    
    # Effectuer l'agrégation
    aggregated_df = messages_df.merge(users_df[['id', 'name']], left_on='user_id', right_on='id')
    aggregated_df = aggregated_df[['name', 'message']]
    

    
    return aggregated_df

# Fonction pour stocker le fichier CSV agrégé dans un bucket S3
def store_csv_file(df):
    # Nom du bucket de destination et du fichier agrégé CSV
    destination_bucket_name = 'pipeline-aggre-result-data-bucket-md4-api'
    aggregated_file_name = 'pipeline_result.csv'
    
    # Convertir le DataFrame agrégé en CSV
    aggregated_csv = df.to_csv(index=False)
    
    # Écrire le fichier agrégé CSV dans le bucket de destination
    s3.Object(destination_bucket_name, aggregated_file_name).put(Body=aggregated_csv)

# Interface Streamlit
st.title('Récupération et stockage de fichiers CSV')
st.write('Cette application récupère les fichiers CSV "users.csv" et "messages.csv" depuis le bucket "sylvaind-raw-data-bucket-md4-api" et stocke le résultat agrégé dans le bucket "pipeline-aggre-result-data-bucket-md4-api".')

# Bouton pour récupérer les fichiers CSV et afficher les résultats
if st.button('Récupérer les fichiers CSV'):
    # Récupérer les fichiers CSV et effectuer l'agrégation
    aggregated_df = get_csv_files()
    
    # Afficher les résultats dans Streamlit
    st.write('Résultats de l\'agrégation :')
    st.write(aggregated_df)

    # Bouton pour stocker le fichier CSV agrégé dans un bucket S3
    if st.button('Stocker le fichier CSV agrégé dans un bucket S3'):
        # Stocker le fichier CSV agrégé dans un bucket S3
        store_csv_file(aggregated_df)
        st.write('Le fichier CSV agrégé a été stocké dans le bucket "pipeline-aggre-result-data-bucket-md4-api".')
