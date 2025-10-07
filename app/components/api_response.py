# app/components/api_response.py

import streamlit as st

from datetime import datetime
import json
import re

def _strip_trackers(html: str) -> str:
    """Remove tracking images and styles from HTML."""
    return re.sub(r'<img[^>]*display:none;[^>]*>', '', html, flags=re.IGNORECASE) if html else html

def _first_dict(*candidates):
    """Return the first non-empty dictionary from the candidates."""
    for c in candidates:
        if isinstance(c, dict) and c:
            return c
    return None

def _fmt_dt(s: str) -> str:
    """Format datetime string to a more readable format."""
    try:
        return datetime.fromisoformat(s.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
    except Exception:
        return s

def _dur(start: str, end: str) -> str:
    """Calculate duration in hours between two datetime strings."""
    try:
        a = datetime.fromisoformat(start.replace('Z', '+00:00'))
        b = datetime.fromisoformat(end.replace('Z', '+00:00'))
        h = (b - a).total_seconds() / 3600
        return f'{h:.1f}h'
    except Exception:
        return ''

def _table_freeblocks(data: dict, max_rows: int = None):
    """Render a table of freeblocks with email, start, end, and duration."""
    rows = list()
    for email, slots in (data or dict()).items():
        for s in slots:
            rows.append({
                'email': email,
                'start': _fmt_dt(s.get('start', '')),
                'end': _fmt_dt(s.get('end', '')),
                'dur': _dur(s.get('start', ''), s.get('end', ''))
            })
    if not rows:
        st.write('—')
        return
    if max_rows and len(rows) > max_rows:
        st.caption(f'Showing {max_rows}/{len(rows)} rows')
        rows = rows[:max_rows]
    else:
        st.caption(f'Total: {len(rows)} slots')
    st.dataframe(rows, use_container_width=True, hide_index=True)

def _slots_block(text: str | None):
    """Render a block of text with slots, removing empty lines."""
    if not text:
        st.write('—')
        return
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    st.code('\n'.join(lines))

def _best_slots_section(best_slots: dict | None):
    """Render the best proposed slots section with details."""
    if not best_slots:
        st.write('—')
        return
    
    selected = best_slots.get('selected', False)
    proposed_slots = best_slots.get('proposed_slots', [])
    feedback = best_slots.get('feedback', '')
    proposal_type = best_slots.get('proposal_type', '')
    matched_reference = best_slots.get('matched_reference', [])
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(f"""
            <span style='
                background: {'#2e7d32' if selected else '#c62828'};
                color: white;
                padding: 5px 12px;
                border-radius: 6px;
                font-weight: bold;
            '>
                {'✓ SELECTED' if selected else '✗ NOT SELECTED'}
            </span>
        """, unsafe_allow_html=True)
        
        if proposal_type:
            st.caption(f"Type: **{proposal_type}**")
    
    with col2:
        if selected and proposed_slots:
            st.markdown("**🎯 Selected slots:**")
            # Handle new format: [[ejecutivo, horario], ...] or legacy format: [horario, ...]
            if isinstance(proposed_slots, list) and proposed_slots:
                formatted_slots = []
                for slot in proposed_slots:
                    if isinstance(slot, list) and len(slot) >= 2:
                        # New format: [ejecutivo, horario]
                        formatted_slots.append(f"{slot[1]} (👤 {slot[0]})")
                    elif isinstance(slot, str):
                        # Legacy format: just horario string
                        formatted_slots.append(slot)
                    else:
                        formatted_slots.append(str(slot))
                slots_text = '\n'.join(formatted_slots)
            else:
                slots_text = str(proposed_slots)
            st.success(slots_text)
        elif not selected:
            st.warning("No viable slots found")
    
    if feedback:
        st.markdown("**💬 AI Feedback:**")
        st.info(feedback)
    
    if matched_reference:
        with st.expander("📋 Matched reference slots"):
            # Ensure all items are strings before joining
            if isinstance(matched_reference, list):
                ref_text = '\n'.join(str(item) for item in matched_reference)
            else:
                ref_text = str(matched_reference)
            st.code(ref_text)

def _badges(status: bool, aiw: dict | None, clf: dict | None):
    """Render badges for status, AI worth, and classification."""
    cols = st.columns(3)

    with cols[0]:
        st.markdown(f"""
            <span style='
                background: {'#2e7d32' if status else '#c62828'};
                color: white;
                padding: 3px 10px;
                border-radius: 6px;
            '>
                {'OK' if status else 'FAIL'}
            </span>
            """,
            unsafe_allow_html=True
        )

    with cols[1]:
        if aiw:
            ok = aiw.get('is_ai_worth')
            st.markdown(f"""
                <span style='
                    background: {'#1565c0' if ok else '#424242'};
                    color: white;
                    padding: 3px 10px;
                    border-radius: 6px;
                '>
                    AI Worth: {str(ok).upper()}
                </span>
                """,
                unsafe_allow_html=True
            )

    with cols[2]:
        if clf:
            st.markdown(f"""
                <span style='
                    background: #6a1b9a;
                    color: white;
                    padding: 3px 10px;
                    border-radius: 6px;
                '>
                    {clf.get('strategy', '?')}:{clf.get('subcategory', '?')}
                </span>
                """,
                unsafe_allow_html=True
            )

def api_response(status_code: int, text: str, json_obj: dict | None, request_payload: dict):
    """Render the API response with status, reply, and various details."""
    st.subheader(f'Status {status_code}')

    if not json_obj:
        st.code(text)
        return

    top_status = json_obj.get('status')
    reply = json_obj.get('reply') or dict()
    raw = json_obj.get('raw_response') or dict()
    inner = raw.get('raw_response') or dict()

    clf = _first_dict(raw.get('classification_response'), inner.get('classification_response'))
    aiw = _first_dict(raw.get('ai_worth_response'), inner.get('ai_worth_response'))
    metrics = _first_dict(json_obj.get('metrics'), raw.get('metrics'), inner.get('metrics'))
    payload = _first_dict(raw.get('payload'), inner.get('payload'))
    payload_after = _first_dict(raw.get('payload_after_slots'), inner.get('payload_after_slots'))
    freeblocks = _first_dict(raw.get('freeblocks'), inner.get('freeblocks'))
    decisions = _first_dict(raw.get('decisions'), inner.get('decisions'))
    best_slots = _first_dict(raw.get('best_proposed_slots'), inner.get('best_proposed_slots'))
    formatted_freeblocks = _first_dict(raw.get('formatted_freeblocks'), inner.get('formatted_freeblocks'))

    _badges(top_status, aiw, clf)

    if reply:
        st.markdown('**Reply to:** ' + str(reply.get('to', '')))
        clean = _strip_trackers(reply.get('body', ''))
        with st.expander('Reply (rendered)', expanded=True):
            st.markdown(clean, unsafe_allow_html=True)
        with st.expander('Reply (HTML)'):
            st.code(reply.get('body', ''), language='html')

    tabs = st.tabs([
        'Summary', 'Calendar & Slots', 'Classification', 'AI Worth', 'Decisions', 'Payloads', 'Raw'
    ])

    with tabs[0]:
        if clf:
            st.write(
                f"Strategy: {clf.get('strategy')} → {clf.get('subcategory')}  | "
                f"Mood: {clf.get('mood')}  | Confidence: {clf.get('confidence')}"
            )
        if aiw:
            st.write(
                f"AI Worth: {aiw.get('is_ai_worth')}  | "
                f"Potential: {aiw.get('meeting_potential')}  | "
                f"Confidence: {aiw.get('confidence')}"
            )
        if metrics:
            st.write('Metrics:', metrics)

    with tabs[1]:
        st.subheader('📅 Calendar & Slots Analysis')
        
        # Best Proposed Slots (AI-optimized)
        st.markdown('### 🎯 Best Proposed Slots (AI-optimized)')
        _best_slots_section(best_slots)
        
        st.divider()
        
        # Final formatted slots used in email
        st.markdown('### 📧 Final Slots for Email')
        if clf and clf.get('proposed_slots'):
            _slots_block(clf.get('proposed_slots'))
        else:
            st.write('—')
        
        st.divider()
        
        # All available freeblocks
        st.markdown('### 📊 All Available Freeblocks')
        if freeblocks:
            if isinstance(freeblocks, str):
                st.text(freeblocks)
            else:
                _table_freeblocks(freeblocks)
        else:
            st.write('—')
        
        st.divider()
        
        st.markdown('### 📊 Formatted Freeblocks')
        st.text(formatted_freeblocks)
        
        
        # Debug information
        with st.expander("🔍 Debug Info - Calendar Query & Configuration"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Query Parameters:**")
                if best_slots:
                    timeslot_analysis = best_slots.get('timeslot_analysis', {})
                    if timeslot_analysis:
                        query_params = timeslot_analysis.get('query_params', {})
                        st.write(f"**Start Date:** {query_params.get('start_date', 'N/A')}")
                        st.write(f"**Days:** {query_params.get('days', 'N/A')}")
                        st.write(f"**Slot Type:** {timeslot_analysis.get('slot_type', 'N/A')}")
                    else:
                        st.write("—")
                else:
                    st.write("No timeslot analysis available")
            
            with col2:
                st.markdown("**⚙️ Calendar Config:**")
                # Try to extract config from payload
                if payload:
                    from_email = payload.get('from', '')
                    domain = from_email.split('@')[-1] if '@' in from_email else 'unknown'
                    st.write(f"**Domain:** {domain}")
                    # This will be in the raw response if available
                st.write("Check 'Payloads' tab for full config")
            
            st.divider()
            
            if freeblocks:
                st.markdown("**📅 Raw Freeblocks (from Google Calendar API):**")
                st.caption("These are the FREE time slots returned by Google Calendar after removing busy periods")
                st.json(freeblocks)
                
                # Count total slots
                total_slots = sum(len(slots) for slots in freeblocks.values())
                st.info(f"Total free slots: {total_slots}")
            else:
                st.warning("⚠️ No freeblocks data available")

    with tabs[2]:
        if clf:
            st.json(clf)
            if clf.get('mentioned_emails'):
                st.write('Mentioned emails:', clf['mentioned_emails'])
        else:
            st.write('—')

    with tabs[3]:
        st.json(aiw) if aiw else st.write('—')

    with tabs[4]:
        if isinstance(decisions, list) and decisions:
            rows = list()
            for d in decisions:
                rows.append({
                    'status': '✅' if d.get('status') else '❌',
                    'strategy': d.get('strategy', '—'),
                    'score': d.get('score', '—'),
                    'feedback': d.get('feedback') or '—'
                })
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.write('—')

    with tabs[5]:
        c1, c2 = st.columns(2)
        with c1:
            st.caption('payload')
            st.json(payload) if payload else st.write('—')
        with c2:
            st.caption('payload_after_slots')
            st.json(payload_after) if payload_after else st.write('—')
        
        if metrics:
            st.divider()
            st.caption('metrics')
            st.json(metrics)

    with tabs[6]:
        st.code(json.dumps(json_obj, indent=2, ensure_ascii=False), language='json')

    with st.expander('Request sent'):
        st.code(json.dumps(request_payload, indent=2, ensure_ascii=False), language='json')
