# app/src/prompts.py

import streamlit as st

from src.gcs import read_text, write_text, list_files_with_prefix

def load_prompt_file(prompt_name):
    """Load a prompt file from GCS."""
    return read_text(
        st.secrets['gcs']['bucket'],
        f'{st.secrets["gcs"]["prompts_folder"]}/{prompt_name}.py'
    )

def save_prompt_file(prompt_name, code):
    """Save a prompt file to GCS."""
    write_text(
        st.secrets['gcs']['bucket'],
        f'{st.secrets["gcs"]["prompts_folder"]}/{prompt_name}.py',
        code,
        content_type='text/x-python'
    )

def list_prompt_files():
    """List all prompt files in GCS."""
    return list_files_with_prefix(
        st.secrets['gcs']['bucket'],
        st.secrets['gcs']['prompts_folder'],
        '.py'
    )

def get_prompt_file_tree():
    """Return a nested dict representing the prompts folder tree."""
    files = [x for x in list_prompt_files() if 'init' not in x]
    root_prefix = st.secrets['gcs']['prompts_folder'].rstrip('/') + '/'
    tree = dict()
    for path in files:
        rel_path = path.removeprefix(root_prefix)
        parts = rel_path.split('/')
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, dict())
        node[parts[-1]] = path
    return tree
