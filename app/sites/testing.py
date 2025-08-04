# app/sites/testing.py

import streamlit as st

import requests
import json

from src.layout import setup_layout, protect_page
from components import api_form, api_response
from src.gcs import fetch_id_token

setup_layout(page_title='ChatTGP - AI Testing')
user = protect_page('editor')

st.title('AI Endpoint Testing')

left_col, right_col = st.columns([1,2])
with left_col:
    submitted, payload = api_form()

if submitted:
    service_url = st.secrets['api']['base_url']
    endpoint = 'zero_effort/classify'
    id_token = fetch_id_token(service_url)
    url = f'{service_url}/{endpoint}'
    headers = {'Authorization': f'Bearer {id_token}','Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        try:
            resp_json = response.json()
        except json.JSONDecodeError:
            resp_json = None
        with right_col:
            api_response(response.status_code, response.text, resp_json, payload)
    except Exception as e:
        with right_col:
            st.error(f'API Error: {e}')
