# app/src/utils.py

import streamlit as st

import re

def error_and_redirect(message: str, target: str):
    """Display an error message and redirect to a target page."""
    if '_redirecting' not in st.session_state:
        st.session_state['_redirecting'] = True
        st.error(message)
        st.session_state['_force_page'] = target
        st.rerun()

def domain_to_blob(input_value: str, client_dir: str, ext: str) -> str:
    if '@' in input_value:
        input_value = input_value.split('@')[-1]
    input_value = input_value.strip().lower()
    domain = re.sub(r'[^a-z0-9.-]', '', input_value)
    domain = domain.strip('.')
    prefix = client_dir.rstrip('/') + '/'
    return f"{prefix}{domain.replace('.', '-')}{ext}"

def blob_to_domain(blob_name: str, client_dir: str, ext: str) -> str:
    raw = blob_name.removeprefix(client_dir).removesuffix(ext)
    return raw.replace('-', '.')
