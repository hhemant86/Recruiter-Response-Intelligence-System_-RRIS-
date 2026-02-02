import os
import sys

def verify_system():
    print("🔍 RRIS Integrity Audit Starting...")
    
    # 1. Check Folder Structure
    required_folders = ['auth', 'email_engine', 'config']
    for folder in required_folders:
        if os.path.exists(folder):
            print(f"✅ Folder Found: {folder}")
        else:
            print(f"❌ MISSING FOLDER: {folder}")

    # 2. Check Critical Files
    critical_files = [
        'main.py',
        '.env',
        'config/credentials.json',
        'email_engine/classifier.py',
        'email_engine/extractor.py',
        'email_engine/state_manager.py',
        'email_engine/__init__.py'
    ]
    for file in critical_files:
        if os.path.exists(file):
            print(f"✅ File Found: {file}")
        else:
            print(f"❌ MISSING FILE: {file}")

    # 3. Test Imports (The "Handshake" Test)
    print("\n🧪 Testing Internal Imports...")
    try:
        from email_engine.classifier import classify_email
        from email_engine.extractor import extract_entities, normalize_text
        from email_engine.state_manager import get_application_id
        print("✅ Internal Logic Handshake: SUCCESS")
    except ImportError as e:
        print(f"❌ IMPORT ERROR: {e}")
        print("   Check if you renamed your files correctly and added __init__.py")

    print("\n🚀 Audit Complete.")

if __name__ == "__main__":
    verify_system()