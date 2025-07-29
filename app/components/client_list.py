# app/components/client_list.py

import streamlit as st

from src.gcs import list_files_with_prefix, write_text
from src.utils import domain_to_blob, blob_to_domain

BUCKET = st.secrets['gcs']['bucket']
CLIENT_DIR = st.secrets['gcs']['clients_folder']
EXT = '.txt'

def client_list():
    blobs = list_files_with_prefix(BUCKET, CLIENT_DIR, EXT)
    domains = sorted([blob_to_domain(b, CLIENT_DIR, EXT) for b in blobs])

    st.subheader('Existing Clients')
    selected = st.radio('Select a client', domains, key='selected_domain') if domains else None

    st.divider()
    st.subheader('Add New Client')
    new_domain = st.text_input('Domain or Email(e.g., tgp.cl or hola@tgp.cl)')
    if st.button('Create'):
        if not new_domain.strip():
            st.warning('Please enter a valid domain or email.')
        else:
            blob_name = domain_to_blob(new_domain, CLIENT_DIR, EXT)
            if blob_name in blobs:
                st.warning('This client already exists.')
            else:
                write_text(BUCKET, blob_name, '', content_type='text/plain')
                st.success(f'{new_domain} created. Reload to edit.')
                st.rerun()

    return selected
