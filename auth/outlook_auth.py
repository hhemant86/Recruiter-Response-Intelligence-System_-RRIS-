# auth/outlook_auth.py
import msal
import os
import atexit
from dotenv import load_dotenv

load_dotenv()

# Define where the session will be saved
CACHE_PATH = os.path.join('config', 'token_cache.bin')

def get_token():
    client_id = os.getenv("MS_CLIENT_ID")
    tenant_id = os.getenv("MS_TENANT_ID", "common")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scopes = ["https://graph.microsoft.com/Mail.Read"]

    # 1. Initialize the Cache Manager
    cache = msal.SerializableTokenCache()
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            cache.deserialize(f.read())

    # 2. Auto-save the cache when the script finishes
    atexit.register(lambda: 
        open(CACHE_PATH, "w").write(cache.serialize()) if cache.has_state_changed else None
    )

    app = msal.PublicClientApplication(client_id, authority=authority, token_cache=cache)

    # 3. Try to get token SILENTLY (No Login)
    accounts = app.get_accounts()
    if accounts:
        # This checks the bin file and refreshes the token automatically
        result = app.acquire_token_silent(scopes, account=accounts[0])
        if result:
            print("✅ Session restored from cache (No login required)")
            return result['access_token']

    # 4. If no cache or expired, do the one-time Device Flow
    print("🔐 Session expired or first run. Please authenticate:")
    flow = app.initiate_device_flow(scopes=scopes)
    print(flow["message"])
    result = app.acquire_token_by_device_flow(flow)
    
    return result.get("access_token")