# app/components/client_py_list.py

import streamlit as st

from src.clients import get_client_files, create_new_client_file

def client_py_list():
    """Component that allows to select a client configuration file (.py) from GCS."""
    client_names = get_client_files()

    st.subheader('Existing Client Configurations')

    selected = None
    if client_names:
        selected = st.radio(
            'Select a client configuration', 
            client_names, 
            key='selected_client_py',
            format_func=lambda x: x.replace('-', '.')  # Display as domain format
        )

    st.divider()

    st.subheader('Add New Client Configuration')

    new_client = st.text_input(
        'Client name (e.g., thegrowth-pro, influence-cl)', 
        placeholder="client-name"
    )

    if st.button('Create New Configuration'):
        if not new_client.strip():
            st.warning('Please enter a valid client name.')
        elif new_client in client_names:
            st.warning('This client configuration already exists.')
        else:
            # Validate format (should be lowercase with hyphens)
            if not new_client.replace('-', '').replace('_', '').isalnum():
                st.warning('Client name should only contain letters, numbers, and hyphens.')
            else:
                try:
                    create_new_client_file(new_client.lower())
                    st.success(f'Created configuration for {new_client}. Refresh to edit.')
                    st.rerun()
                except Exception as e:
                    st.error(f'Error creating client configuration: {e}')

    return selected

