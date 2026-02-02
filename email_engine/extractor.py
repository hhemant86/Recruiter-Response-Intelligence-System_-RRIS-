# email_engine/extractor.py
import re

def normalize_text(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

def extract_entities(subject, body, sender_email=""):
    # 1. Try Subject Patterns
    match = re.search(r"at\s+([A-Z][A-Za-z0-9\s&]+)", subject)
    if match:
        return match.group(1).strip().title(), "Position"

    # 2. BRUTE FORCE: Look at the email domain (e.g., careers@honeycomb.io)
    if "@" in sender_email:
        domain = sender_email.split("@")[-1].split(".")[0]
        if domain not in ["gmail", "outlook", "hotmail", "yahoo"]:
            return domain.title(), "Position"

    return "Unknown Company", "Position"