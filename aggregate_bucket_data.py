import boto3
import pandas as pd
import io


# Informations d'identification AWS
AWS_ACCESS_KEY_ID = 'AKIA2BHJHJTWXQQZBRUC'
AWS_SECRET_ACCESS_KEY = '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'

# Noms des buckets
SOURCE_BUCKET_NAME = 'sylvaind-raw-data-bucket-md4-api'
RESULT_BUCKET_NAME = 'pipeline-aggre-result-data-bucket-md4-api'

# Nom des fichiers à récupérer
MESSAGES_FILE_NAME = 'messages.csv'
USERS_FILE_NAME = 'users.csv'

# Nom des colonnes après agrégation
COLUMN_MAPPING = {
    'author_id': 'user_id',
    'first_name': 'name',
    'content': 'message'
}

# Colonnes à conserver dans le fichier de résultat
RESULT_COLUMNS = ['user_id', 'name', 'message']

# Initialisation du client S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def download_file(bucket_name, file_name):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        data = response['Body'].read().decode('utf-8')
        return pd.read_csv(io.StringIO(data))
    except Exception as e:
        print(f"Une erreur s'est produite lors du téléchargement du fichier {file_name} : {e}")
        return None

def upload_file(bucket_name, file_name, dataframe):
    try:
        buffer = io.StringIO()
        dataframe.to_csv(buffer, index=False)
        s3_client.put_object(Body=buffer.getvalue(), Bucket=bucket_name, Key=file_name)
        print(f"Le fichier {file_name} a été téléchargé avec succès sur le bucket {bucket_name} !")
        return True
    except Exception as e:
        print(f"Une erreur s'est produite lors du téléchargement du fichier {file_name} sur le bucket {bucket_name} : {e}")
        return False

# Téléchargement des fichiers depuis le bucket source
messages_data = download_file(SOURCE_BUCKET_NAME, MESSAGES_FILE_NAME)
users_data = download_file(SOURCE_BUCKET_NAME, USERS_FILE_NAME)

# Vérification des téléchargements
if messages_data is None or users_data is None:
    print("Erreur lors du téléchargement des fichiers. Arrêt du programme.")
    exit()

# Renommage des colonnes
messages_data = messages_data.rename(columns=COLUMN_MAPPING)
users_data = users_data.rename(columns=COLUMN_MAPPING)

# Fusion des données
result_data = pd.merge(messages_data, users_data, on='user_id', how='left')

# Sélection des colonnes requises
result_data = result_data[RESULT_COLUMNS]

# Enregistrement du fichier de résultat dans le bucket de destination
upload_file(RESULT_BUCKET_NAME, 'pipeline_result.csv', result_data)
