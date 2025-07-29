# app/components/auth_form.py

import streamlit as st

from src.auth import load_auth, validate_hmac

def auth_form():
    """Render the authentication form."""

    if 'user' in st.session_state:
        return st.session_state['user']

    with st.form(key='auth_form'):
        st.title('ChatTGP Authentication')
        email = st.text_input('Email', placeholder='Enter your email')
        api_key = st.text_input('API Key', placeholder='Enter your API key', type='password')
        submit_button = st.form_submit_button('Login')

    if not submit_button:
        st.stop()

    email = email.strip().lower()
    auth_data = load_auth()
    auth_entry = auth_data.get(email)

    if not auth_entry:
        st.error('No account found for this email.')
        st.stop()

    if validate_hmac(email, api_key, st.secrets['security']['master_key']):
        st.session_state['user'] = {**auth_entry, 'email': email}
        st.success('Login successful!')
        st.rerun()

    st.error('Invalid API key. Please try again.')
    st.stop()
