# app/src/auth.py

import streamlit as st

import hashlib
import hmac

from src.gcs import read_json, write_json

def hmac_hash(email: str, master_key: str) -> str:
    """Generate HMAC hash for the given email and master key."""
    return hmac.new(master_key.encode(), email.lower().encode(), hashlib.sha256).hexdigest()

def validate_hmac(email: str, key: str, master_key: str) -> bool:
    """Validate HMAC key against the stored auth entry."""
    return hmac.compare_digest(hmac_hash(email, master_key).encode(), key.encode())

def load_auth():
    """Load authentication data from Google Cloud Storage."""
    return read_json(st.secrets['gcs']['bucket'], st.secrets['gcs']['auth_file'])

def save_auth(data: dict):
    """Save authentication data to Google Cloud Storage."""
    write_json(st.secrets['gcs']['bucket'], st.secrets['gcs']['auth_file'], data)

def has_permission(user: dict, permission: str) -> bool:
    """Check if the user has the specified permission."""
    return permission in user.get('permissions', list())
