import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from database.sheet_manager import connect_to_db

def generate_dashboard():
    print("\n🚀 Initializing RRIS Executive Intelligence Report...")
    sheet = connect_to_db()
    if not sheet: return

    # 1. Load Data
    data = sheet.get_all_records()
    if not data:
        print("📭 The Sheet is currently empty. Run 'python main.py --deep' first!")
        return

    df = pd.DataFrame(data)

    # 🛠️ THE NORMALIZER: Force all headers to lowercase and strip spaces
    df.columns = [c.strip().lower() for c in df.columns]

    # 2. Required Columns Validation (Lowercase Version)
    required = ['first seen', 'status', 'company', 'role']
    missing = [col for col in required if col not in df.columns]
    
    if missing:
        print(f"❌ Error: Missing columns in Sheet: {missing}")
        print(f"💡 Found these headers: {df.columns.tolist()}")
        print("👉 Please ensure headers include: Company, Role, Status, First Seen")
        return

    # 3. Data Processing
    df['first seen'] = pd.to_datetime(df['first seen'], errors='coerce')
    total_apps = len(df)
    
    # Normalize status column content to lowercase for reliable matching
    df['status_clean'] = df['status'].str.lower().str.strip()
    
    # Define Funnel Stages
    viewed_mask = df['status_clean'].isin(['viewed', 'interview', 'rejected', 'replied'])
    interview_mask = df['status_clean'].isin(['interview', 'confirmed'])
    rejection_mask = df['status_clean'] == 'rejected'
    
    viewed_count = len(df[viewed_mask])
    interview_count = len(df[interview_mask])
    rejection_count = len(df[rejection_mask])
    
    # Calculate Conversion Rates
    view_rate = (viewed_count / total_apps * 100) if total_apps > 0 else 0
    interview_rate = (interview_count / total_apps * 100) if total_apps > 0 else 0

    # 4. HEADER & KPIs
    print("\n" + "═"*60)
    print(f"📊 RRIS STRATEGIC DASHBOARD | {datetime.now().strftime('%d %b %Y')}")
    print("═"*60)
    print(f"{'TOTAL PIPELINE SIZE':<30}: {total_apps} Companies")
    print(f"{'RESUME VIEW RATE (ATS PASS)':<30}: {view_rate:.1f}%")
    print(f"{'INTERVIEW CONVERSION':<30}: {interview_rate:.1f}%")
    print(f"{'TOTAL REJECTIONS':<30}: {rejection_count}")

    # 5. 📅 RECENT MOMENTUM
    print("\n" + "──" * 5 + " 📅 RECENT ACTIVITY (TOP 10) " + "──" * 5)
    recent = df.sort_values(by='first seen', ascending=False).head(10)
    for _, row in recent.iterrows():
        date_str = row['first seen'].strftime('%d %b') if pd.notnull(row['first seen']) else "NEW"
        
        # Icon logic based on clean status
        st = row['status_clean']
        icon = "🟢" if "interview" in st or "confirmed" in st else "🔴" if "rejected" in st else "🟡"
        print(f"{date_str} | {icon} {str(row['company'])[:18]:<18} | {str(row['status']):<12} | {str(row['role'])[:20]}")

    # 6. 👻 GHOSTING RISK
    print("\n" + "──" * 5 + " ⚠️ GHOSTING RISK / STALE LEADS " + "──" * 5)
    ten_days_ago = datetime.now() - timedelta(days=10)
    stale_mask = (df['status_clean'].isin(['applied', 'viewed'])) & (df['first seen'] < ten_days_ago)
    stale_leads = df[stale_mask].sort_values(by='first seen')

    if not stale_leads.empty:
        for _, row in stale_leads.head(3).iterrows():
            days_ago = (datetime.now() - row['first seen']).days
            print(f"STALE ({days_ago}d): {str(row['company'])[:15]:<15} -> Consider LinkedIn Follow-up.")
    else:
        print("✅ Pipeline is fresh. All active leads are under 10 days old.")

    # 7. 🧠 AI STRATEGIC INSIGHTS
    print("\n" + "──" * 5 + " 💡 STRATEGIC RECOMMENDATIONS " + "──" * 5)
    if view_rate < 20:
        print("⚡ [ATS ALERT] View rate low. Your Resume might not be hitting the keywords.")
    
    if interview_count > 0:
        print(f"🔥 [MOMENTUM] You have {interview_count} active interview tracks. Focus on Prep!")

    print("═"*60 + "\n")

if __name__ == "__main__":
    generate_dashboard()