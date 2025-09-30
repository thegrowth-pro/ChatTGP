# app/sites/prompt_engineering.py

import streamlit as st

from streamlit_ace import st_ace

from src.prompts import get_prompt_file_tree, load_prompt_file, save_prompt_file
from src.layout import setup_layout, protect_page
from components import prompt_tree

setup_layout(page_title='ChatTGP - Prompt Engineering')

user = protect_page('editor')

st.title('Prompt Editor')

tree = get_prompt_file_tree()

def handle_file_select(blob_name):
    st.session_state['selected_prompt'] = blob_name

col_left, col_right = st.columns([1, 3])

with col_left:
    prompt_tree(tree, handle_file_select)

# TODO: Convert the col_right into a component.

with col_right:
    if 'selected_prompt' in st.session_state:
        selected_blob = st.session_state['selected_prompt']
        root_prefix = st.secrets['gcs']['prompts_folder'].rstrip('/')+'/'
        internal_path = selected_blob.removeprefix(root_prefix)
        prompt_name = internal_path.removesuffix('.py')

        st.subheader(f'Editing: `{internal_path}`')

        code = load_prompt_file(prompt_name)

        edited = st_ace(
            value=code,
            language='python',
            theme='solarized_dark',
            keybinding='vscode',
            font_size=14,
            tab_size=4,
            wrap=True,
            show_gutter=True,
            show_print_margin=True,
            height=500,
            key=f'ace_{prompt_name}'
        )

        if st.button('Save'):
            try:
                save_prompt_file(prompt_name, edited)
                st.success(f'✅ Saved `{internal_path}`')
            except Exception as e:
                st.error(f'❌ Error saving `{internal_path}`: {e}')
