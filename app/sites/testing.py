# app/sites/testing.py

import streamlit as st

import requests
import json

from src.layout import setup_layout, protect_page
from components.api_form import api_form, close_thread_form, close_thread_sent_form
from components.api_response import api_response
from src.gcs import fetch_id_token

setup_layout(page_title='ChatTGP - AI Testing')
user = protect_page('editor')


def _display_close_thread_response(status_code: int, text: str, json_obj: dict | None, request_payload: dict):
    """Display response for close thread endpoint."""
    st.subheader(f'Status {status_code}')
    
    if not json_obj:
        st.code(text)
        return
    
    # Main results
    should_close = json_obj.get('status', False)
    close_type = json_obj.get('type')
    reply = json_obj.get('reply', '')
    
    # Display badges
    col1, col2 = st.columns(2)
    with col1:
        if should_close:
            st.success('✅ CLOSE THREAD')
        else:
            st.info('⏳ KEEP OPEN')
    
    with col2:
        if close_type:
            type_colors = {
                'meeting_confirmed': '🎯',
                'spam': '🚫',
                'bounce': '⚠️',
                'unsubscribe': '🔕',
                'other': '📝'
            }
            icon = type_colors.get(close_type, '❓')
            st.info(f'{icon} {close_type.replace("_", " ").title()}')
    
    # Display reason/reply
    if reply:
        st.markdown('**Decision Reason:**')
        st.info(reply)
    
    # Display full response in tabs
    tabs = st.tabs(['Summary', 'Raw Response', 'Request Sent'])
    
    with tabs[0]:
        st.json({
            'should_close': should_close,
            'close_type': close_type,
            'reason': reply
        })
    
    with tabs[1]:
        st.code(json.dumps(json_obj, indent=2, ensure_ascii=False), language='json')
    
    with tabs[2]:
        st.code(json.dumps(request_payload, indent=2, ensure_ascii=False), language='json')


st.title('AI Endpoint Testing')

# Endpoint selector
endpoint_option = st.selectbox(
    'Select Endpoint',
    ['Classification', 'Close Thread - Received Message', 'Close Thread - Sent Message'],
    index=0
)

left_col, right_col = st.columns([1,2])

# Show appropriate form based on selection
with left_col:
    if endpoint_option == 'Classification':
        submitted, payload = api_form()
        endpoint = 'zero_effort/classify'
    elif endpoint_option == 'Close Thread - Received Message':
        submitted, payload = close_thread_form()
        endpoint = 'zero_effort/close_thread_message_received'
    else:  # Close Thread - Sent Message
        submitted, payload = close_thread_sent_form()
        endpoint = 'zero_effort/close_thread_message_sent'

if submitted:
    service_url = st.secrets['api']['base_url']
    id_token = fetch_id_token(service_url)
    url = f'{service_url}/{endpoint}'
    headers = {'Authorization': f'Bearer {id_token}','Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=300)
        try:
            resp_json = response.json()
        except json.JSONDecodeError:
            resp_json = None
        with right_col:
            if endpoint_option == 'Classification':
                api_response(response.status_code, response.text, resp_json, payload)
            else:  # Close Thread (Received or Sent)
                _display_close_thread_response(response.status_code, response.text, resp_json, payload)
    except Exception as e:
        with right_col:
            st.error(f'API Error: {e}')
