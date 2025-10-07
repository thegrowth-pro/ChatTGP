# app/sites/testing.py

import streamlit as st

import requests
import json

from src.layout import setup_layout, protect_page
from components.api_form import api_form, close_thread_form, close_thread_sent_form, create_meeting_form
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
    should_archive = json_obj.get('should_archive', True)
    reply = json_obj.get('reply', '')
    
    # Display badges
    col1, col2, col3 = st.columns(3)
    with col1:
        if should_close:
            st.success('✅ CLOSE THREAD')
        else:
            st.info('⏳ KEEP OPEN')
    
    with col2:
        if close_type:
            type_colors = {
                'conversation_ended': '🎯',
                'spam': '🚫',
                'do_not_reply': '🤖',
                'automatic_mail': '⚙️',
                'bounce': '⚠️'
            }
            icon = type_colors.get(close_type, '❓')
            st.info(f'{icon} {close_type.replace("_", " ").title()}')
    
    with col3:
        if should_close:
            if should_archive:
                st.warning('📦 ARCHIVE')
            else:
                st.success('📬 KEEP UNREAD')
    
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
            'should_archive': should_archive,
            'reason': reply
        })
    
    with tabs[1]:
        st.code(json.dumps(json_obj, indent=2, ensure_ascii=False), language='json')
    
    with tabs[2]:
        st.code(json.dumps(request_payload, indent=2, ensure_ascii=False), language='json')


def _display_create_meeting_response(status_code: int, text: str, json_obj: dict | None, request_payload: dict):
    """Display response for create meeting endpoint."""
    st.subheader(f'Status {status_code}')
    
    if not json_obj:
        st.code(text)
        return
    
    # Extract main components
    payload_sent = json_obj.get('payload_sent', {})
    tgp_app_response = json_obj.get('tgp_app_response', {})
    
    # Success/Error indicator
    if status_code == 200 and tgp_app_response:
        st.success('✅ Meeting Created Successfully!')
    elif status_code == 200:
        st.warning('⚠️ Request processed but no response from TGP App')
    else:
        st.error(f'❌ Error: Status {status_code}')
    
    # Display key information
    if payload_sent:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Prospect', payload_sent.get('prospect_name', 'N/A'))
        with col2:
            st.metric('Company', payload_sent.get('prospect_company_name', 'N/A'))
        with col3:
            st.metric('Date', payload_sent.get('date', 'N/A'))
        
        # Additional details
        st.markdown('**Prospect Information:**')
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📧 **Email:** {', '.join(payload_sent.get('prospect_email', []))}")
            st.info(f"👤 **Role:** {payload_sent.get('prospect_role', 'N/A')}")
        with col2:
            st.info(f"📞 **Phone:** {payload_sent.get('prospect_phone', 'N/A')}")
            st.info(f"🌍 **Country:** {payload_sent.get('country', 'N/A')}")
        
        # Sellers
        sellers = payload_sent.get('sellers', [])
        if sellers:
            st.markdown(f"**👥 Sellers:** {', '.join(sellers)}")
        
        # Meeting settings
        col1, col2 = st.columns(2)
        with col1:
            meet_link = '✅' if payload_sent.get('generateGoogleMeetLink', False) else '❌'
            st.info(f"{meet_link} **Google Meet Link**")
        with col2:
            calendar = '✅' if payload_sent.get('generateGoogleCalendarEvent', False) else '❌'
            st.info(f"{calendar} **Google Calendar Event**")
    
    # Display tabs with detailed information
    tabs = st.tabs(['Summary', 'Payload Sent', 'TGP App Response', 'Request Sent', 'LLM Extraction'])
    
    with tabs[0]:
        summary = {
            'status_code': status_code,
            'success': status_code == 200 and bool(tgp_app_response),
            'prospect_name': payload_sent.get('prospect_name') if payload_sent else None,
            'prospect_company': payload_sent.get('prospect_company_name') if payload_sent else None,
            'meeting_date': payload_sent.get('date') if payload_sent else None,
            'tgp_app_responded': bool(tgp_app_response)
        }
        st.json(summary)
    
    with tabs[1]:
        if payload_sent:
            st.code(json.dumps(payload_sent, indent=2, ensure_ascii=False), language='json')
        else:
            st.warning('No payload sent')
    
    with tabs[2]:
        if tgp_app_response:
            st.code(json.dumps(tgp_app_response, indent=2, ensure_ascii=False), language='json')
        else:
            st.warning('No response from TGP App')
    
    with tabs[3]:
        st.code(json.dumps(request_payload, indent=2, ensure_ascii=False), language='json')
    
    with tabs[4]:
        # Show what the LLM extracted
        if payload_sent:
            extracted = {
                'prospect_company_name': payload_sent.get('prospect_company_name'),
                'prospect_name': payload_sent.get('prospect_name'),
                'prospect_role': payload_sent.get('prospect_role'),
                'prospect_phone': payload_sent.get('prospect_phone'),
                'country': payload_sent.get('country')
            }
            st.markdown('**Data extracted by LLM from email thread:**')
            st.json(extracted)
        else:
            st.warning('No LLM extraction data available')


st.title('AI Endpoint Testing')

# Endpoint selector
endpoint_option = st.selectbox(
    'Select Endpoint',
    ['Classification', 'Close Thread - Received Message', 'Close Thread - Sent Message', 'Create Meeting'],
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
    elif endpoint_option == 'Close Thread - Sent Message':
        submitted, payload = close_thread_sent_form()
        endpoint = 'zero_effort/close_thread_message_sent'
    else:  # Create Meeting
        submitted, payload = create_meeting_form()
        endpoint = 'zero_effort/create_meeting_on_tgp_app'

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
            elif endpoint_option == 'Create Meeting':
                _display_create_meeting_response(response.status_code, response.text, resp_json, payload)
            else:  # Close Thread (Received or Sent)
                _display_close_thread_response(response.status_code, response.text, resp_json, payload)
    except Exception as e:
        with right_col:
            st.error(f'API Error: {e}')
