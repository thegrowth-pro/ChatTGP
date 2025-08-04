# app/components/client_editor.py

import streamlit as st

from src.gcs import read_text, write_text
from src.params import BUCKET, CLIENT_DIR

EXT = '.txt'

def domain_to_blob(domain: str) -> str:
    """Auxiliar function to convert client domain in blob for Google Cloud Storage."""
    return f"{CLIENT_DIR}{domain.lower().replace('.', '-')}{EXT}"

def client_editor(domain: str):
    """Create an editor to edit TGP Client Data files (.txt)."""
    blob_name = domain_to_blob(domain)
    current_text = read_text(BUCKET, blob_name)

    st.subheader(f'Edit: {domain}')
    edited = st.text_area('Content', value=current_text, height=600, key='client_txt')

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Save'):
            write_text(BUCKET, blob_name, edited, content_type='text/plain')
            st.success('Saved.')

    with col2:
        if st.button('Reload'):
            st.session_state['client_txt'] = read_text(BUCKET, blob_name)
            st.info('Reloaded.')
