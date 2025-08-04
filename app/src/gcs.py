# app/src/gcs.py

import streamlit as st

from google.auth.transport import requests as google_requests
from google.oauth2 import service_account
from google.cloud import storage

import json

def _client() -> storage.Client:
    """Create a Google Cloud Storage client."""
    if st.secrets['env']['mode'] == 'cloud':
        return storage.Client(credentials=service_account.Credentials.from_service_account_info(
            st.secrets['gcp_credentials']
        ))
    return storage.Client()

def read_text(bucket_name: str, blob_name: str) -> str:
    """Read text from a blob in a Google Cloud Storage bucket."""
    blob = _client().bucket(bucket_name).blob(blob_name)
    return blob.download_as_text()

def write_text(
    bucket_name: str,
    blob_name: str,
    content: str,
    content_type: str = 'application/json'
):
    """Write text to a blob in a Google Cloud Storage bucket."""
    blob = _client().bucket(bucket_name).blob(blob_name)
    blob.upload_from_string(content, content_type=content_type)

def read_json(bucket_name: str, blob_name: str) -> dict:
    """Read JSON from a blob in a Google Cloud Storage bucket."""
    return json.loads(read_text(bucket_name, blob_name))

def write_json(bucket_name: str, blob_name: str, content: dict):
    """Write JSON to a blob in a Google Cloud Storage bucket."""
    write_text(
        bucket_name,
        blob_name,
        json.dumps(content, indent=4),
        content_type='application/json'
    )

def list_files_with_prefix(bucket_name: str, prefix: str, extension: str) -> list[str]:
    """List files in a Google Cloud Storage bucket with a specific prefix."""
    return [
        blob.name for blob in _client().bucket(bucket_name).list_blobs(prefix=prefix)
        if blob.name.endswith(extension)
    ]

def get_id_token_audience(service_url: str) -> str:
    """Extracts audience for ID token from service URL."""
    return service_url if service_url.startswith('https://') else f'https://{service_url}'

def fetch_id_token(service_url: str) -> str:
    """Generate and cache an ID token using service account credentials."""
    key = f'_id_token::{service_url}'
    if key in st.session_state:
        return st.session_state[key]

    credentials = service_account.IDTokenCredentials.from_service_account_info(
        st.secrets['gcp_credentials'],
        target_audience=get_id_token_audience(service_url)
    )

    credentials.refresh(google_requests.Request())
    st.session_state[key] = credentials.token

    return credentials.token
