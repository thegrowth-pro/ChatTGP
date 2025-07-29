# app/components/session_box.py

import streamlit as st

from uuid import uuid4

def session_box(user, logout_cb):
    """Render the session box in the sidebar."""
    st.session_state.setdefault('_session_uid', str(uuid4()))

    st.markdown("""
    <style>
        .session-wrapper {
            background-color: #1e293b;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            margin-top: 1rem;
            box-shadow: inset 0 0 0 1px #334155;
        }
        .session-wrapper .user-name {
            font-size: 0.9rem;
            font-weight: 600;
            color: #38bdf8;
            margin-bottom: 0.4rem;
            display: block;
        }
        .session-wrapper .role-chip {
            display: inline-block;
            background-color: #0f172a;
            color: #cbd5e1;
            font-size: 0.7rem;
            border-radius: 4px;
            padding: 2px 6px;
        }
        .stButton > button {
            background-color: #ef4444;
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            padding: 0.5rem;
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar.expander('Session', expanded=True):
        st.markdown(f"""
            <div class="session-wrapper" style="margin: 0 0 1rem 0;">
                <span class="user-name">{user.get('name', user.get('email'))}</span>
                <span class="role-chip">{user['role']}</span>
            </div>""",
            unsafe_allow_html=True,
        )
        key = f"logout_{st.session_state['_session_uid']}"
        if st.button('Logout', key=key, use_container_width=True):
            logout_cb()
