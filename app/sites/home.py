# app/sites/home.py

import streamlit as st

from src.layout import setup_layout
from components import auth_form

setup_layout(page_title='ChatTGP')

if 'user' not in st.session_state:
    auth_form()
    st.stop()

user = st.session_state['user']
name = user.get('name', 'User')

st.title(f'Welcome, {name} to ChatTGP!')
