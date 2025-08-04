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

def _table_freeblocks(data: dict, max_rows: int = 30):
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
    if len(rows) > max_rows:
        st.caption(f'Showing {max_rows}/{len(rows)}')
        rows = rows[:max_rows]
    st.dataframe(rows, use_container_width=True, hide_index=True)

def _slots_block(text: str | None):
    """Render a block of text with slots, removing empty lines."""
    if not text:
        st.write('—')
        return
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    st.code('\n'.join(lines))

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

    _badges(top_status, aiw, clf)

    if reply:
        st.markdown('**Reply to:** ' + str(reply.get('to', '')))
        clean = _strip_trackers(reply.get('body', ''))
        with st.expander('Reply (rendered)', expanded=True):
            st.markdown(clean, unsafe_allow_html=True)
        with st.expander('Reply (HTML)'):
            st.code(reply.get('body', ''), language='html')

    tabs = st.tabs([
        'Summary', 'Classification', 'AI Worth', 'Metrics', 'Payloads',
        'Freeblocks', 'Decisions', 'Raw'
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
        if clf:
            st.json(clf)
            st.markdown('**Proposed slots**')
            _slots_block(clf.get('proposed_slots'))
            if clf.get('mentioned_emails'):
                st.write('Mentioned emails:', clf['mentioned_emails'])
        else:
            st.write('—')

    with tabs[2]:
        st.json(aiw) if aiw else st.write('—')

    with tabs[3]:
        st.json(metrics) if metrics else st.write('—')

    with tabs[4]:
        c1, c2 = st.columns(2)
        with c1:
            st.caption('payload')
            st.json(payload) if payload else st.write('—')
        with c2:
            st.caption('payload_after_slots')
            st.json(payload_after) if payload_after else st.write('—')

    with tabs[5]:
        _table_freeblocks(freeblocks)

    with tabs[6]:
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

    with tabs[7]:
        st.code(json.dumps(json_obj, indent=2, ensure_ascii=False), language='json')

    with st.expander('Request sent'):
        st.code(json.dumps(request_payload, indent=2, ensure_ascii=False), language='json')
