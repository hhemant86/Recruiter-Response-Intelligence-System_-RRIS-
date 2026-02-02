# email_engine/state_manager.py
import hashlib

def normalize_role(role_name):
    """Groups similar roles into buckets to prevent duplicates."""
    r = str(role_name).lower()
    if any(x in r for x in ["quant", "researcher", "math", "trading"]): return "Quant"
    if any(x in r for x in ["data", "analyst", "analytics"]): return "Data"
    if any(x in r for x in ["finance", "accountant", "treasury", "controller"]): return "Finance"
    if any(x in r for x in ["developer", "engineer", "software"]): return "Engineering"
    return "General"

def get_application_id(company, role):
    """Generates ID based on Company + Normalized Category."""
    comp = str(company).strip().lower()
    role_grp = normalize_role(role)
    unique_string = f"{comp}|{role_grp}"
    return hashlib.sha1(unique_string.encode()).hexdigest()