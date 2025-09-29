# app/components/client_py_editor.py

import streamlit as st
from streamlit_ace import st_ace

from src.clients import load_client_file, save_client_file

def client_py_editor(client_name: str):
    """Create an editor to edit client configuration files (.py) using ACE editor."""
    
    try:
        # Load current code
        current_code = load_client_file(client_name)
        
        st.subheader(f'Editing: `{client_name}.py`')
        
        # Display client name as domain format for reference
        domain_format = client_name.replace('-', '.')
        st.caption(f'Client domain: **{domain_format}**')
        
        # ACE Editor for Python code
        edited_code = st_ace(
            value=current_code,
            language='python',
            theme='solarized_dark',
            keybinding='vscode',
            font_size=14,
            tab_size=4,
            wrap=True,
            show_gutter=True,
            show_print_margin=True,
            height=500,
            key=f'ace_client_{client_name}'
        )

        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button('💾 Save', use_container_width=True):
                try:
                    save_client_file(client_name, edited_code)
                    st.success(f'✅ Saved `{client_name}.py`')
                except Exception as e:
                    st.error(f'❌ Error saving: {e}')

        with col2:
            if st.button('🔄 Reload', use_container_width=True):
                try:
                    # Force reload by removing from session state
                    if f'ace_client_{client_name}' in st.session_state:
                        del st.session_state[f'ace_client_{client_name}']
                    st.rerun()
                except Exception as e:
                    st.error(f'❌ Error reloading: {e}')

        # Preview section
        st.divider()
        
        with st.expander("📋 Template Reference"):
            st.code('''
CLIENT_CONFIG = {
    "description": """
    [Descripción del cliente]
    
    Servicios principales:
    - [Servicio 1]
    - [Servicio 2]
    
    [Información adicional]
    """,
    
    "calendar_rules": """
    Horario de atención: 8:00 a 18:00
    Almuerzo: 14:00 a 15:00
    Días no disponibles: miércoles
    Zona horaria: America/Santiago
    """
}
            ''', language='python')

        # Validation warnings
        if 'CLIENT_CONFIG' not in edited_code:
            st.warning('⚠️ Make sure your file contains `CLIENT_CONFIG` dictionary.')
        
        if '"description"' not in edited_code:
            st.warning('⚠️ Make sure `CLIENT_CONFIG` contains a `"description"` field.')
            
        if '"calendar_rules"' not in edited_code:
            st.warning('⚠️ Make sure `CLIENT_CONFIG` contains a `"calendar_rules"` field.')

    except Exception as e:
        st.error(f'❌ Error loading client configuration: {e}')
        st.info('💡 The file might not exist yet. Try creating it first.')

