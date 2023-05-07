import streamlit as st
import boto3
import pandas as pd
import io

AWS_ACCESS_KEY_ID = 'AKIA2BHJHJTWXQQZBRUC'
AWS_SECRET_ACCESS_KEY = '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'
RESULT_BUCKET_NAME = 'pipeline-aggre-result-data-bucket-md4-api'
RESULT_FILE_NAME = 'pipeline_result.csv'

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def getFileFromBucket(file_name, bucket_name):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        data = response['Body'].read().decode('utf-8')
        return pd.read_csv(io.StringIO(data))
    except Exception as e:
        st.error(f"An error occurred while getting the file from S3 bucket: {e}")
        return None

file = getFileFromBucket(RESULT_FILE_NAME, RESULT_BUCKET_NAME)

if file is not None:
    st.header("Résultat du pipeline")
    st.write(file)
else:
    st.error("Failed to download the pipeline_result.csv file from S3!")
