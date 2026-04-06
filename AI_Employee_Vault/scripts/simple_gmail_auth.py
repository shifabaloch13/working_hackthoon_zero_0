"""
Simple Gmail Authentication

This creates a simple OAuth flow for Gmail.
"""

import os
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the token.pickle file.
SCOPES = [
    'https://mail.google.com/'  # Full access (includes send)
]

def main():
    creds = None
    
    # The file token.pickle stores the user's access and refresh tokens
    token_path = Path('gmail_token.pickle')
    
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Path to your credentials.json file
            cred_path = Path('../../credeintals.json')
            
            if not cred_path.exists():
                print("❌ Error: credeintals.json not found!")
                print("Please download it from Google Cloud Console")
                return
            
            print("=" * 70)
            print("  GMAIL AUTHENTICATION")
            print("=" * 70)
            print()
            print("Opening browser for authentication...")
            print()
            print("STEPS:")
            print("  1. Browser will open")
            print("  2. Sign in with your Google account")
            print("  3. Grant ALL permissions")
            print("  4. Return here when done")
            print()
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(cred_path), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        
        print()
        print("=" * 70)
        print("  ✅ AUTHENTICATION SUCCESSFUL!")
        print("=" * 70)
        print()
        print("Token saved to: gmail_token.pickle")
        print()
        print("You can now send emails!")
        print()
    else:
        print("✅ Already authenticated!")
        print("Token found: gmail_token.pickle")

if __name__ == '__main__':
    main()
