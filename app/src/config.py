# app/src/config.py

import streamlit as st

from src.gcs import read_json, write_json

def load_config():
    """Load configuration from GCS."""
    return read_json(
        st.secrets['gcs']['bucket'],
        st.secrets['gcs']['config_file']
    )

def save_config(data: dict):
    """Save configuration to GCS."""
    write_json(
        st.secrets['gcs']['bucket'],
        st.secrets['gcs']['config_file'],
        data
    )
