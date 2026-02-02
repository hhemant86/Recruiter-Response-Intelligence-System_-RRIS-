import msal
import requests

CLIENT_ID = "5a666919-10c2-4ff4-a392-80e7f8ec7c6e"  # YOUR CLIENT ID

print("🔐 LOGIN...")
app = msal.PublicClientApplication(CLIENT_ID, authority="https://login.microsoftonline.com/common")

flow
