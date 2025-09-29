# app/src/clients.py

import streamlit as st

from src.gcs import read_text, write_text, list_files_with_prefix

def load_client_file(client_name):
    """Load a client configuration file from GCS."""
    return read_text(
        st.secrets['gcs']['bucket'],
        f'clients/{client_name}.py'
    )

def save_client_file(client_name, code):
    """Save a client configuration file to GCS."""
    write_text(
        st.secrets['gcs']['bucket'],
        f'clients/{client_name}.py',
        code,
        content_type='text/x-python'
    )

def list_client_files():
    """List all client configuration files in GCS."""
    return list_files_with_prefix(
        st.secrets['gcs']['bucket'],
        'clients',
        '.py'
    )

def get_client_files():
    """Return a list of client names from GCS."""
    files = list_client_files()
    client_names = []
    for file in files:
        # Extract client name from path like 'clients/thegrowth-pro.py'
        if file.startswith('clients/') and file.endswith('.py'):
            client_name = file.removeprefix('clients/').removesuffix('.py')
            client_names.append(client_name)
    return sorted(client_names)

def create_new_client_file(client_name):
    """Create a new client configuration file with template."""
    template = '''# chat-tgp/clients/{client_name}.py

CLIENT_CONFIG = {{
    "description": """
    [Agregar descripción del cliente aquí]
    
    [Información adicional sobre el cliente]
    """,
    
    "calendar_rules": """
    [Agregar reglas de calendario específicas del cliente aquí]
    
    Ejemplo:
    - Horario de atención: 8:00 a 18:00
    - Almuerzo: 14:00 a 15:00
    - Días no disponibles: miércoles
    - Zona horaria: America/Santiago
    """
}}'''.format(client_name=client_name)
    
    save_client_file(client_name, template)
    return template

