# app/sites/home.py

import streamlit as st

from components import auth_form
from src.layout import setup_layout

setup_layout(page_title='ChatTGP')

if 'user' not in st.session_state:
    auth_form()
    st.stop()

user = st.session_state['user']
name = user.get('name', 'User')

st.title(f'Welcome, {name} to ChatTGP!')
