# scripts/create_api_key.py

import hashlib
import hmac
import sys

def create_api_key(email: str, master_key: str) -> str:
    """Create an HMAC API key for the given email and master key."""
    return hmac.new(master_key.encode(), email.lower().encode(), hashlib.sha256).hexdigest()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python create_api_key.py <email> <master_key>')
        sys.exit(1)
    print(f'API Key for {sys.argv[1]}: {create_api_key(sys.argv[1], sys.argv[2])}')
