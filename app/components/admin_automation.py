# app/components/admin_automation.py

import streamlit as st

import re

from src.gcs import read_json, write_json
from src.params import BUCKET, CONFIG_DIR
DOMAIN_RX = re.compile(r'^[a-z0-9.-]+\.[a-z]{2,}$', re.I)

def admin_automation():
    """Component that allows to modify GCS Admin Config File for Mail Handler automation."""

    if 'automation_cfg' not in st.session_state:
        st.session_state.automation_cfg = read_json(BUCKET, CONFIG_DIR)
    
    cfg = st.session_state.automation_cfg
    auto = cfg.get('automation', {'enabled': False, 'whitelist': list()})

    if 'automation_wl' not in st.session_state:
        st.session_state.automation_wl = list(dict.fromkeys(auto.get('whitelist', list())))
    if 'automation_enabled_state' not in st.session_state:
        st.session_state.automation_enabled_state = auto.get('enabled', False)

    wl = st.session_state.automation_wl

    st.subheader('Automation')
    st.session_state.automation_enabled_state = st.toggle(
        'enabled',
        value=st.session_state.automation_enabled_state,
        key='automation_enabled'
    )

    st.markdown('#### Whitelist')
    left, right = st.columns([0.48, 0.52])

    # TODO: Divide these columns in two component (left/right in different files).

    with left:

        c1, c2 = st.columns([0.7, 0.3])
        new_domain = c1.text_input(
            'add_domain', placeholder='thegrowth.pro', label_visibility='collapsed'
        )

        if c2.button('Add', key='automation_add'):
            d = (new_domain or '').strip().lower()
            if d:
                if not DOMAIN_RX.match(d):
                    st.error('Invalid domain format')
                elif d not in wl:
                    wl.append(d)
                    st.rerun()

        if st.button('Save', key='automation_save'):
            cfg['automation'] = {
                'enabled': st.session_state.automation_enabled_state,
                'whitelist': wl
            }
            write_json(BUCKET, CONFIG_DIR, cfg)
            st.session_state.automation_cfg = cfg
            st.success('Saved successfully')

    with right:

        to_delete = list()

        for i, d in enumerate(wl):
            r2, r1 = st.columns([0.1, 0.8])
            r1.markdown(f'<span style="font-size:0.9rem;">`{d}`</span>', unsafe_allow_html=True)
            if r2.button('🗑️', key=f'automation_delete_{i}'):
                to_delete.append(d)
        
        if to_delete:
            st.session_state.automation_wl = [d for d in wl if d not in to_delete]
            st.rerun()

    st.markdown("""
    <style>
    .stButton button {
        margin: 0 !important;
        padding: 3px 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)
