# email_engine/fetch_emails.py
import requests
from datetime import datetime, timedelta

def fetch_emails(token):
    headers = {"Authorization": f"Bearer {token}"}
    cutoff = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    folders = ["inbox", "junkemail", "sentitems"]
    all_emails = []
    
    for folder in folders:
        print(f"📡 Deep Scanning {folder} for full content...")
        url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder}/messages"
        # We now select 'body' to get the HTML content of the entire email
        params = {
            "$filter": f"receivedDateTime ge {cutoff}",
            "$select": "id,subject,from,receivedDateTime,body", 
            "$top": 50 
        }
        
        while url:
            try:
                resp = requests.get(url, headers=headers, params=params)
                if resp.status_code != 200: break
                data = resp.json()
                all_emails.extend(data.get("value", []))
                url = data.get("@odata.nextLink")
                params = None 
            except: break
                
    return all_emails