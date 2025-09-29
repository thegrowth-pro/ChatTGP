# app/sites/client_config.py

import streamlit as st

from src.layout import setup_layout, protect_page
from components import client_py_list, client_py_editor

setup_layout(page_title='ChatTGP - Client Configuration')
user = protect_page('editor')

st.title('Client Configuration Editor')

st.markdown("""
📝 **Edit client configuration files** that define:
- **Description**: Information about the client and their services
- **Calendar Rules**: Meeting availability and scheduling preferences

These configurations are used by the AI to provide personalized responses.
""")

left, right = st.columns([0.35, 0.65])

with left:
    selected_client = client_py_list()

with right:
    if selected_client:
        client_py_editor(selected_client)
    else:
        st.info("📋 Select or create a client configuration to edit.")
        
        st.markdown("""
        ### 🎯 How it works:
        
        1. **Select** a client from the list on the left
        2. **Edit** their configuration using the Python editor  
        3. **Save** your changes to update the AI behavior
        
        ### 📋 Configuration Format:
        
        Each client file contains a `CLIENT_CONFIG` dictionary with:
        - `description`: Company info, services, and context
        - `calendar_rules`: Meeting hours, restrictions, and preferences
        
        ### 🔗 Integration:
        
        These configurations are automatically loaded by:
        - Zero Effort Classification system
        - Meeting proposal AI
        - Email response generation
        """)

