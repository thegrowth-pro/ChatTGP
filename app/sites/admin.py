# app/sites/admin.py

import streamlit as st

from components import admin_automation
from src.layout import setup_layout

setup_layout(page_title='ChatTGP - Admin Panel')

st.title('Admin Panel')

admin_automation()
