# app/sites/client_data.py

import streamlit as st

from src.layout import setup_layout, protect_page
from components import client_list, client_editor

setup_layout(page_title='ChatTGP - Client Data')
user = protect_page('editor')

st.title('Client Data')

left, right = st.columns([0.35, 0.65])

with left:
    selected_domain = client_list()

with right:
    if selected_domain:
        client_editor(selected_domain)
    else:
        st.info("Select or create a domain to edit the content.")

