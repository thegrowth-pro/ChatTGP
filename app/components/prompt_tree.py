# app/components/prompt_tree.py

import streamlit as st

def prompt_tree(tree: dict, on_select):
    """Render a collapsible file tree and invoke `on_select(blob_name)` when a file is clicked."""
    def _render(tree, parent_key=''):
        for key, value in tree.items():
            if isinstance(value, dict):
                with st.expander(f'📁 {key}', expanded=True):
                    _render(value, parent_key + key + '/')
            else:
                if st.button(f'📝 {key}', key=parent_key + key):
                    on_select(value)
    _render(tree)
