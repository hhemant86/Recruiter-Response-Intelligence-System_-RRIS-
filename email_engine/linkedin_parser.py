# email_engine/linkedin_parser.py

def parse_linkedin_rejection(subject, body):
    text = f"{subject} {body}".lower()
    
    if "linkedin" not in text:
        return None

    rejection_phrases = [
        "will not be moving forward", 
        "unfortunately", 
        "decided to move forward with other",
        "not moving forward with your application"
    ]

    if not any(p in text for p in rejection_phrases):
        return None

    # Logic for: "Your update from Alpha Access Limited"
    company = "Unknown"
    if "update from" in subject.lower():
        company = subject.lower().split("update from")[-1].strip().title()
    elif "application to" in subject.lower():
        # Fallback for: "Your application to [Role] at [Company]"
        parts = subject.lower().split(" at ")
        if len(parts) > 1:
            company = parts[-1].strip().title()

    return {
        "company": company,
        "status": "Rejected",
        "role": "Quantitative Researcher" # Standardizing for Alpha Access
    }