# app/components/admin_automation.py

import streamlit as st

import json
import re

from src.gcs import read_json, write_json
from src.params import BUCKET, CONFIG_DIR
DOMAIN_RX = re.compile(r'^[a-z0-9.-]+\.[a-z]{2,}$', re.I)

def admin_automation():
    """Component that allows to modify GCS Admin Config File for Mail Handler automation."""

    if 'automation_cfg' not in st.session_state:
        st.session_state.automation_cfg = read_json(BUCKET, CONFIG_DIR)
    
    cfg = st.session_state.automation_cfg
    auto = cfg.get('automation', {'automationlist': list(), 'draftlist': list()})

    if 'automationlist' not in st.session_state:
        st.session_state.automationlist = list(dict.fromkeys(auto.get('automationlist', list())))
    if 'draftlist' not in st.session_state:
        st.session_state.draftlist = list(dict.fromkeys(auto.get('draftlist', list())))

    st.subheader('Automation')
    
    edit_mode = st.radio(
        "Modo de edición:",
        ["UI", "Raw JSON"],
        horizontal=True,
        key="automation_edit_mode"
    )
    
    if edit_mode == "Raw JSON":
        st.markdown("#### Editar JSON directamente")
        
        current_json = json.dumps(cfg.get('automation', {}), indent=2)
        
        edited_json = st.text_area(
            "Configuración JSON:",
            value=current_json,
            height=200,
            help="Edita la configuración directamente en formato JSON"
        )
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if st.button("Guardar JSON", key="save_raw_json"):
                try:
                    new_automation_config = json.loads(edited_json)
                    
                    cfg['automation'] = new_automation_config
                    write_json(BUCKET, CONFIG_DIR, cfg)
                    st.session_state.automation_cfg = cfg
                    
                    st.session_state.automationlist = list(dict.fromkeys(new_automation_config.get('automationlist', [])))
                    st.session_state.draftlist = list(dict.fromkeys(new_automation_config.get('draftlist', [])))
                    
                    st.success("✅ JSON guardado exitosamente")
                    st.rerun()
                    
                except json.JSONDecodeError as e:
                    st.error(f"❌ Error en el formato JSON: {e}")
                except Exception as e:
                    st.error(f"❌ Error al guardar: {e}")
        
        with col2:
            if st.button("Validar JSON", key="validate_json"):
                try:
                    json.loads(edited_json)
                    st.success("✅ JSON válido")
                except json.JSONDecodeError as e:
                    st.error(f"❌ JSON inválido: {e}")
        
        st.markdown("---")
        
    else:
        
        st.markdown('#### Automation List (envío automático)')
        auto_left, auto_right = st.columns([0.48, 0.52])

        with auto_left:
            c1, c2 = st.columns([0.7, 0.3])
            new_auto_domain = c1.text_input(
                'add_auto_domain', placeholder='thegrowth.pro', label_visibility='collapsed'
            )

            if c2.button('Add', key='automation_add'):
                d = (new_auto_domain or '').strip().lower()
                if d:
                    if not DOMAIN_RX.match(d):
                        st.error('Invalid domain format')
                    elif d not in st.session_state.automationlist:
                        st.session_state.automationlist.append(d)
                        st.rerun()

        with auto_right:
            auto_to_delete = list()
            for i, d in enumerate(st.session_state.automationlist):
                r2, r1 = st.columns([0.1, 0.8])
                r1.markdown(f'<span style="font-size:0.9rem;">`{d}`</span>', unsafe_allow_html=True)
                if r2.button('🗑️', key=f'automation_delete_{i}'):
                    auto_to_delete.append(d)
            
            if auto_to_delete:
                st.session_state.automationlist = [d for d in st.session_state.automationlist if d not in auto_to_delete]
                st.rerun()

        st.markdown('#### Draft List (solo borradores)')
        draft_left, draft_right = st.columns([0.48, 0.52])

        with draft_left:
            c1, c2 = st.columns([0.7, 0.3])
            new_draft_domain = c1.text_input(
                'add_draft_domain', placeholder='example.com', label_visibility='collapsed'
            )

            if c2.button('Add', key='draft_add'):
                d = (new_draft_domain or '').strip().lower()
                if d:
                    if not DOMAIN_RX.match(d):
                        st.error('Invalid domain format')
                    elif d not in st.session_state.draftlist:
                        st.session_state.draftlist.append(d)
                        st.rerun()

        with draft_right:
            draft_to_delete = list()
            for i, d in enumerate(st.session_state.draftlist):
                r2, r1 = st.columns([0.1, 0.8])
                r1.markdown(f'<span style="font-size:0.9rem;">`{d}`</span>', unsafe_allow_html=True)
                if r2.button('🗑️', key=f'draft_delete_{i}'):
                    draft_to_delete.append(d)
            
            if draft_to_delete:
                st.session_state.draftlist = [d for d in st.session_state.draftlist if d not in draft_to_delete]
                st.rerun()

        if st.button('Save', key='automation_save'):
            cfg['automation'] = {
                'automationlist': st.session_state.automationlist,
                'draftlist': st.session_state.draftlist
            }
            write_json(BUCKET, CONFIG_DIR, cfg)
            st.session_state.automation_cfg = cfg
            st.success('Saved successfully')

    st.markdown("""
    <style>
    .stButton button {
        margin: 0 !important;
        padding: 3px 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)
