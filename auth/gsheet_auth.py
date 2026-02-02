# auth/gsheet_auth.py
import gspread
from google.oauth2.service_account import Credentials
import os

def connect_sheet(sheet_name):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds_path = os.path.join('config', 'credentials.json')
    
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"Missing: {creds_path}. Place your Google JSON key in config/ folder.")

    try:
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Try to open the sheet; if it fails, give a clear error
        try:
            return client.open(sheet_name).sheet1
        except gspread.exceptions.SpreadsheetNotFound:
            raise Exception(f"Error: Spreadsheet '{sheet_name}' not found. Check the name and Share it with the bot email.")
            
    except Exception as e:
        raise Exception(f"Cloud Connection Failed: {str(e)}")