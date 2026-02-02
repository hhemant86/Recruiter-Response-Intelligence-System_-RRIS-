# database/sheet_manager.py
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("config/credentials.json", scope)
    client = gspread.authorize(creds)
    sheet_name = os.getenv("GOOGLE_SHEET_NAME", "Job_Intelligence_DB")
    sheet = client.open(sheet_name).sheet1
    return sheet

def update_or_append(sheet, data, app_id, email_date):
    # This prevents the "Duplicate Header" error by being specific
    all_values = sheet.get_all_values()
    if not all_values:
        headers = ["S.No", "Company", "Job Title", "Status", "First Seen", "Last Updated", "Application_ID"]
        sheet.append_row(headers)
        all_values = [headers]

    headers = all_values[0]
    records = [dict(zip(headers, row)) for row in all_values[1:]]
    now = datetime.now().strftime("%Y-%m-%d")
    
    # Deduplication Check
    for i, row in enumerate(records, 2):
        if str(row.get('Application_ID')) == str(app_id):
            if row.get('Status') != "Rejected":
                sheet.update_cell(i, 4, data['status'])
                sheet.update_cell(i, 6, email_date) # Update 'Last Updated' with email date
                print(f"🔄 Updated: {data['company']}")
            return False

    # Add New Row
    s_no = len(records) + 1
    new_row = [s_no, data['company'], data['role'], data['status'], email_date, email_date, app_id]
    sheet.append_row(new_row)
    print(f"✨ New Entry: {data['company']}")
    return True