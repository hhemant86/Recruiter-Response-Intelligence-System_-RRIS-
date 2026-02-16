# email_engine/fetch_emails.py
import requests
from datetime import datetime, timedelta

def fetch_emails(token, days_back=60):
    """
    Fetches emails from Outlook with a dynamic lookback window.
    :param token: Microsoft Graph Access Token
    :param days_back: Number of days to look back (default 60)
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    # Calculate the dynamic cutoff date based on the days_back parameter
    cutoff = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    folders = ["inbox", "junkemail", "sentitems"]
    all_emails = []
    
    for folder in folders:
        print(f"📡 Scanning {folder} (Since {cutoff[:10]})...")
        url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder}/messages"
        
        # OData parameters for efficient fetching
        params = {
            "$filter": f"receivedDateTime ge {cutoff}",
            "$select": "id,subject,from,receivedDateTime,body", 
            "$top": 50 
        }
        
        while url:
            try:
                resp = requests.get(url, headers=headers, params=params)
                if resp.status_code != 200:
                    print(f"❌ API Error in {folder}: {resp.status_code}")
                    break
                
                data = resp.json()
                batch = data.get("value", [])
                all_emails.extend(batch)
                
                # Check if there's another page of results
                url = data.get("@odata.nextLink")
                params = None # Parameters are already included in the nextLink
                
            except Exception as e:
                print(f"⚠️ Fetch Error: {e}")
                break
                
    return all_emails