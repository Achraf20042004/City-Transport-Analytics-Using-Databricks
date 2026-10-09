# Databricks notebook source
import boto3
import os

# 1. Connexion à MinIO (exposé par ngrok), identifiants dans le secret scope "minio"
s3 = boto3.client('s3',
                  endpoint_url=dbutils.secrets.get("minio", "endpoint_url"),
                  aws_access_key_id=dbutils.secrets.get("minio", "access_key"),
                  aws_secret_access_key=dbutils.secrets.get("minio", "secret_key"))

# 2. Dossier du Volume lu par Auto Loader
local_dir = "/Volumes/transportation/bronze/datasource/1. data/trips/Full Load/"
os.makedirs(local_dir, exist_ok=True)

# 3. Téléchargement des fichiers du bucket
objects = s3.list_objects_v2(Bucket='transportation')
for obj in objects.get('Contents', []):
    file_key = obj['Key']
    s3.download_file('transportation', file_key, local_dir + file_key)
