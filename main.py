import sys
import time
from tqdm import tqdm
from auth.outlook_auth import get_token
from email_engine.fetch_emails import fetch_emails
from email_engine.processor import analyze_job_email_llm
from email_engine.signal_filter import is_real_job_email
from email_engine.linkedin_parser import parse_linkedin_rejection
from database.sheet_manager import connect_to_db, update_or_append
from email_engine.state_manager import get_application_id

def run_sync(deep_scan=False):
    """
    RRIS Core Sync Engine: Orchestrates email fetching, filtering, 
    AI analysis, and database updates.
    """
    mode_text = "DEEP SCAN MODE (60 Days)" if deep_scan else "FAST SYNC MODE (3 Days)"
    print(f"\n🚀 Starting RRIS AI Sync | {mode_text}")
    print("═" * 50)
    
    # 1. Initialize Connections
    sheet = connect_to_db()
    if not sheet: 
        print("❌ Database connection failed. Aborting.")
        return
        
    token = get_token()
    days_to_fetch = 60 if deep_scan else 3
    
    # 2. Fetch Signals
    emails = fetch_emails(token, days_back=days_to_fetch) 
    total_emails = len(emails)
    
    if total_emails == 0:
        print("📭 No new emails found in the specified window.")
        return

    print(f"📡 Found {total_emails} potential signals. Starting processing...\n")

    # 3. Process with Progress Bar
    # Use tqdm to track iterations and estimated time remaining (ETA)
    for mail in tqdm(emails, desc="📥 Syncing Applications", unit="email", leave=True):
        subject = mail.get('subject', '')
        body = mail.get('body', '') 
        sender = mail.get('from', {}).get('emailAddress', {}).get('address', 'Unknown')
        
        # Standardize date for the tracker
        email_date_raw = mail.get('receivedDateTime', '')
        email_date = email_date_raw.split('T')[0] if email_date_raw else "2026-02-16"

        # LAYER 1: Hard Filter (The Bouncer)
        if not is_real_job_email(subject, body, sender):
            continue

        # LAYER 2: Fast Regex Parsing (LinkedIn Specialist)
        li_hit = parse_linkedin_rejection(subject, body)
        if li_hit:
            app_id = get_application_id(li_hit["company"], li_hit["role"])
            update_or_append(sheet, li_hit, app_id, email_date)
            continue

        # LAYER 3: LLM Contextual Analysis (The Genius)
        extracted = analyze_job_email_llm(subject, body, sender)
        
        # Only commit if AI actually identified a legitimate company
        if extracted.get('company') and extracted['company'] not in ["Unknown", ""]:
            app_id = get_application_id(extracted['company'], extracted['role'])
            update_or_append(sheet, extracted, app_id, email_date)
            
            # 🔥 RATE LIMIT PROTECTION: 
            # 2s sleep ensures we stay within Groq Free Tier TPM/RPM limits.
            time.sleep(2) 

    print(f"\n" + "═" * 50)
    print(f"✅ Sync Complete. {mode_text} finished successfully.")

if __name__ == "__main__":
    # Check terminal arguments for deep scan flag
    is_deep = "--deep" in sys.argv
    run_sync(deep_scan=is_deep)