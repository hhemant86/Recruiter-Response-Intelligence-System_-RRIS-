import asyncio
import re
from portal_engine.portal_crawler import get_portal_intelligence
from email_engine.processor import analyze_job_email_llm
from database.sheet_manager import connect_to_db, update_or_append
from email_engine.state_manager import get_application_id
from datetime import datetime

def extract_url(text):
    """Finds the first URL in a string of text."""
    url = re.search(r'(https?://[^\s]+)', text)
    return url.group(0) if url else None

async def sync_portals():
    print("🕵️ Starting RRIS Portal Intelligence Sync...")
    sheet = connect_to_db()
    if not sheet: return

    # 1. Fetch all applications from the sheet
    records = sheet.get_all_records()
    today = datetime.now().strftime('%Y-%m-%d')

    for row in records:
        # 2. Logic: Only crawl if we have a URL and the status isn't 'Rejected'
        reasoning = row.get('Reasoning', '') or row.get('reasoning', '')
        status = row.get('Status', '') or row.get('status', '')
        
        url = extract_url(reasoning)
        
        if url and status != "Rejected":
            print(f"🔍 Checking {row['Company']} via portal...")
            
            # 3. Use your Intelligent Crawler
            raw_text = await get_portal_intelligence(url)
            
            if raw_text:
                # 4. Use the upgraded AI Processor to 'read' the page
                # We pass the url as the 'sender' for context
                analysis = analyze_job_email_llm("Portal Status Update", raw_text, url)
                
                if analysis['status'] != "Noise":
                    app_id = get_application_id(analysis['company'], analysis['role'])
                    update_or_append(sheet, analysis, app_id, today)
                    print(f"✅ Updated {analysis['company']} status to {analysis['status']}")

    print("🏁 Portal Sync Complete.")

if __name__ == "__main__":
    asyncio.run(sync_portals())