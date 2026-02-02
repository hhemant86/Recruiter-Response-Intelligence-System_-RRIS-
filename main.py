# main.py
from auth.outlook_auth import get_token
from email_engine.fetch_emails import fetch_emails
from email_engine.processor import analyze_job_email_llm
from email_engine.signal_filter import is_real_job_email
from email_engine.linkedin_parser import parse_linkedin_rejection
from database.sheet_manager import connect_to_db, update_or_append
from email_engine.state_manager import get_application_id

def run_sync():
    print("🚀 Starting RRIS AI Sync (Deep Scan Mode)...")
    
    # Initialize Database and Microsoft Connection
    sheet = connect_to_db()
    token = get_token()
    
    # Fetch 60 days of emails using the paginated fetcher
    emails = fetch_emails(token) 
    
    for mail in emails:
        # --- DATA EXTRACTION ---
        subject = mail.get('subject', '')
        body = mail.get('body', '') 
        sender = mail.get('from', {}).get('emailAddress', {}).get('address', 'Unknown')
        
        # EXTRACT DATE: Converts '2026-01-28T14:00:00Z' to '2026-01-28'
        email_date_raw = mail.get('receivedDateTime', '')
        email_date = email_date_raw.split('T')[0] if email_date_raw else "2026-02-02"

        # --- LAYER 1: THE BOUNCER (Hard Filter) ---
        # Kills noise (SIPs, GitHub, Newsletters) immediately
        if not is_real_job_email(subject, body, sender):
            continue

        # --- LAYER 2: THE SPECIALIST (LinkedIn Parser) ---
        # Catches hybrid templates like Alpha Access rejections
        li_hit = parse_linkedin_rejection(subject, body)
        if li_hit:
            print(f"🎯 LinkedIn Detection: {li_hit['company']}")
            # Uses Fix 3: Normalized Role Deduplication
            app_id = get_application_id(li_hit["company"], li_hit["role"])
            # FIX: Properly passing email_date to prevent TypeError
            update_or_append(sheet, li_hit, app_id, email_date)
            continue

        # --- LAYER 3: THE GENIUS (Local Ollama LLM) ---
        # Handles complex extraction for Turing, HoneyComb, CoinDCX, etc.
        print(f"💻 AI Analyzing (Full Context): {subject[:40]}...")
        extracted = analyze_job_email_llm(subject, body, sender)
        
        if extracted['company'] != "Unknown":
            # Uses Fix 3: Normalized Role Deduplication
            app_id = get_application_id(extracted['company'], extracted['role'])
            # FIX: Properly passing email_date to prevent TypeError
            update_or_append(sheet, extracted, app_id, email_date)

    print("✅ Sync Complete. System is now Historically Accurate and Clean.")

if __name__ == "__main__":
    run_sync()