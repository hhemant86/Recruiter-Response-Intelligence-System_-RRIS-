import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

load_dotenv()

# Define the Rank of Statuses (Higher is better)
STATUS_RANK = {
    "Noise": 0,
    "Viewed": 1,
    "Applied": 2,
    "Replied": 3,
    "Interview": 4,
    "Confirmed": 5,
    "Selected": 6,
    "Rejected": -1  # Terminal state
}

def connect_to_db():
    try:
        sheet_name = os.getenv("GOOGLE_SHEET_NAME")
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_path = os.path.join('config', 'credentials.json')
        creds = Credentials.from_service_account_file(creds_path, scopes=scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open(sheet_name)
        return spreadsheet.get_worksheet(0)
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def update_or_append(sheet, extracted_data, app_id, email_date):
    """
    Supercoach Logic:
    1. Prevents "Noise" from being written.
    2. Enforces "Forward-Only" status updates.
    3. Terminal State Lock (Rejected/Selected).
    """
    try:
        status = extracted_data.get('status', 'Viewed')
        company = extracted_data.get('company', 'Unknown')
        role = extracted_data.get('role', 'Not Specified')
        
        # 🛡️ GATE 1: NOISE ELIMINATION
        if status == "Noise" or company == "Unknown":
            # Silently ignore noise to keep logs clean
            return "Ignored Noise"

        existing_ids = sheet.col_values(7) 
        
        if app_id in existing_ids:
            row_index = existing_ids.index(app_id) + 1
            current_status = sheet.cell(row_index, 3).value or "Viewed"
            
            # 🛡️ GATE 2: STATE MACHINE LOCK
            # Don't update if current status is terminal (Rejected/Selected)
            if current_status in ["Rejected", "Selected"]:
                return "Locked State"

            # 🛡️ GATE 3: PROGRESSION CHECK
            # Only update if the new status is 'higher' in the career ladder
            current_rank = STATUS_RANK.get(current_status, 0)
            new_rank = STATUS_RANK.get(status, 0)

            if new_rank > current_rank:
                print(f"📈 Progression: {company} | {current_status} -> {status}")
                sheet.update_cell(row_index, 3, status)
                sheet.update_cell(row_index, 6, email_date) # Last Update
                # Refine reasoning to be concise
                sheet.update_cell(row_index, 4, f"Updated: {status} on {email_date}")
            return "Status Improved"
        
        else:
            # 🛡️ GATE 4: FIRST-TIME WRITE
            # Only append if it's a real company/role
            new_row = [
                company, 
                role, 
                status, 
                extracted_data.get('reasoning', 'Initial entry')[:100], # Cap reasoning length
                email_date, # First Seen
                email_date, # Last Update
                app_id
            ]
            sheet.append_row(new_row)
            print(f"✨ NEW APPLICATION: {company} for {role}")
            return "Appended"

    except Exception as e:
        print(f"❌ Logic Error: {e}")
        return "Error"