import re

def extract_portal_links(email_body):
    """
    Supercoach Utility:
    Scans the email body for known recruitment portals.
    """
    if not email_body:
        return []

    # Patterns for the most common application tracking systems (ATS)
    patterns = [
        r'https?://[^\s<>"]*turing\.com/[^\s<>"]*',
        r'https?://[^\s<>"]*lever\.co/[^\s<>"]*',
        r'https?://[^\s<>"]*greenhouse\.io/[^\s<>"]*',
        r'https?://[^\s<>"]*myworkdayjobs\.com/[^\s<>"]*',
        r'https?://[^\s<>"]*ashbyhq\.com/[^\s<>"]*',
        r'https?://[^\s<>"]*smartrecruiters\.com/[^\s<>"]*'
    ]
    
    found_links = []
    for pattern in patterns:
        matches = re.findall(pattern, email_body)
        found_links.extend(matches)
        
    # Remove duplicates and return
    return list(set(found_links))