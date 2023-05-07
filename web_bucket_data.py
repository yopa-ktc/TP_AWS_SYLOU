import streamlit as st
import boto3
import os
import sys
import pandas as pd
from dotenv import load_dotenv
import io
from io import StringIO, BytesIO
from botocore.exceptions import ClientError

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_MESSAGE_BUCKET = os.getenv('S3_MESSAGE_BUCKET')
S3_LEADERBOARD_BUCKET = os.getenv('S3_LEADERBOARD_BUCKET')


if AWS_ACCESS_KEY_ID is None or AWS_SECRET_ACCESS_KEY is None:
    print('AWS crendentials are missing...')
    sys.exit(-1)

s3client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

upload, messages, leaderboard = st.tabs(["Telecharger fichier", "Messages", "Leaderboard"])

def uploadFileToBucket(file_object, file_name, bucket_name):
    try:
        s3client.upload_fileobj(file_object, bucket_name, file_name)
        return True
    except ClientError as e:
        st.error(f"Une erreur s'est produite lors du téléchargement du fichier sur le bucket S3 : {e}")
        return False

# utilisez boto3 pour télécharger le tampon de fichiers dans le compartiment S3
# gérer les erreurs avec un try..except sur le boto ClientError


def getFileFromBucket(file_name, bucket_name):
# utilisez boto3 pour obtenir l'objet du compartiment S3
# gérer les erreurs avec un try..except sur le boto ClientError
    return False
    
    
def computeLeaderboard():
# téléchargez messages.csv depuis S3_MESSAGE_BUCKET et enregistrez-le dans une base de données
# créer un nouveau dataframe où les utilisateurs sont regroupés avec leur nombre de messages
# transformer la dataframe en buffer (n'oubliez pas la fonction seek(0))
# vérifier avec boto si le S3_LEADERBOARD_BUCKET existe déjà et sinon le créer
# téléchargez le tampon vers S3_LEADERBOARD_BUCKET dans l'objet leaderboard.csv (utilisez uploadFileToBucket)
    return False

with upload:
    st.header("Télécharger des données sur S3")
    uploaded_file = st.file_uploader("Choisir un fichier")
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        if st.button('Télécharger sur S3'):
            uploaded_file.seek(0)
            success = uploadFileToBucket(uploaded_file, 'messages.csv', 'sylvaind-raw-data-bucket-md4-api')
            if success:
                st.text(f"Le fichier messages.csv a été téléchargé avec succès sur le bucket 'sylvaind-raw-data-bucket-md4-api' !")
            else:
                st.text('Échec du téléchargement !')


with messages:
    st.header("Messages dataset")
    file = getFileFromBucket('messages.csv', S3_MESSAGE_BUCKET)
    if file is not False:
        st.write(pd.read_csv(file))
        if st.button('Compute leaderboard'):
            result = computeLeaderboard()
            if result is not False:
                st.text('Calcul effectué!')
            else:
                st.text('Calcul echoué!')
    else:
        st.text('echec du telechargement!')

with leaderboard:
    st.header("leaderboard utilisateur")
    file = getFileFromBucket('leaderboard.csv', S3_LEADERBOARD_BUCKET)
    if file is not False:
        st.write(pd.read_csv(file))
    else:
        st.text('Echec Telechargement!')
    if st.button('Rafraichir'):
            file = getFileFromBucket('leaderboard.csv', S3_LEADERBOARD_BUCKET)
            if file is not False:
                 st.text('Telechargé avec succes!')
            else:
                st.text('Echec telechargement!')