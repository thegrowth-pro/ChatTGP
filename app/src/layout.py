# app/src/layout.py

import streamlit as st

from src.params import PATHS, GITHUB_URL, REPORT_URL_MAIL, ABOUT_TEXT
from src.utils import error_and_redirect
from components import session_box

def setup_layout(page_title: str):
    """Set up the layout for the Streamlit app."""
    st.set_page_config(
        layout='wide',
        page_title=page_title,
        page_icon=PATHS['favicon'],
        initial_sidebar_state='expanded',
        menu_items={
            'Get Help': GITHUB_URL,
            'Report a bug': REPORT_URL_MAIL,
            'About': ABOUT_TEXT,
        },
    )

    st.logo(
        image=PATHS['logo'],
        link=GITHUB_URL,
    )
    if 'user' in st.session_state:
        session_box(st.session_state['user'], logout)

    st.markdown("""
        <style>
            [data-testid="stMainBlockContainer"] {
                padding: 0px 50px;
            }
            [data-testid="stSidebarLogo"] {
                display: block;
                margin: 0px;
                width: auto;
                height: 75px;
            }
            [data-testid="stSidebarHeader"] {
                padding: 0px;
                margin: 20px 0px 32px 11px; /* top, right, bottom, left */
                height: 75px;
            }
            [data-testid="stSidebarNav"] {
                margin-top: 0px !important;
            }
        </style>
    """, unsafe_allow_html=True)

def protect_page(required_role: str = None) -> dict:
    """Protect page and return user if authenticated and authorized."""
    if 'user' not in st.session_state:
        error_and_redirect('You must be logged in.', 'home')
        st.stop()

    user = st.session_state['user']
    role = user.get('role', '')

    if required_role == 'admin' and role != 'admin':
        error_and_redirect('You must be an admin to access this page.', 'home')
        st.stop()

    elif required_role == 'editor' and role not in ('admin', 'editor'):
        error_and_redirect('You must be an admin or editor.', 'home')
        st.stop()

    return user

def logout():
    st.session_state.clear()
    st.session_state['_force_page'] = 'home'
    st.session_state['_redirecting'] = True
    st.rerun()

def setup_pages():
    """Set up the pages for the Streamlit app."""
    if st.session_state.get('_redirecting'):
        st.session_state.pop('_redirecting')
        st.rerun()

    if '_force_page' in st.session_state:
        st.session_state['__st_navigation_current_page__'] = st.session_state.pop('_force_page')

    current_slug = st.session_state.get('__st_navigation_current_page__', 'home')
    user = protect_page() if current_slug != 'home' else st.session_state.get('user')

    pages = {
        'Home': [
            st.Page(PATHS['pages']['home'], title='Home', icon='🚀'),
            st.Page(PATHS['pages']['docs'], title='Documentation', icon='📚'),
        ]
    }

    if user:
        pages['Home'].append(
            st.Page(PATHS['pages']['logs'], title='Logs', icon='📜')
        )

    if user and user['role'] == 'admin':
        pages['Admin'] = [
            st.Page(PATHS['pages']['admin'], title='Admin Panel', icon='🔧'),
            st.Page(PATHS['pages']['user_settings'], title='User Management', icon='👤'),
            st.Page(PATHS['pages']['client_settings'], title='Client Settings', icon='💸'),
            st.Page(PATHS['pages']['local'], title='Cloud Deploy (Local Mode)', icon='⚙️'),
        ]

    if user and user['role'] in ('admin', 'editor'):
        pages['Editor'] = [
            st.Page(PATHS['pages']['prompt_engineering'], title='Prompt Engineering', icon='📝'),
            st.Page(PATHS['pages']['client_data'], title='Client Data', icon='📊'),
            st.Page(PATHS['pages']['testing'], title='AI Testing', icon='🔍'),
        ]

    nav = st.navigation(pages)
    nav.run()
