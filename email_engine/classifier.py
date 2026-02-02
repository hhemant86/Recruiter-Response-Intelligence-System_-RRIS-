# engine/classifier.py

def classify_email(subject, body):
    """
    AIS Intent Classifier. 
    Replaces is_job_related with high-signal state detection.
    """
    text = f"{subject} {body}".lower()

    # 1. THE SECURITY WALL (Your Blacklist)
    # If it's a security alert, ignore it immediately.
    security_noise = ["security code", "new sign-in", "verify your account", "password changed"]
    if any(item in text for item in security_noise):
        return "IGNORE"

    # 2. PRIORITY 1: REJECTIONS
    # High-signal words that mean the application is closed.
    if any(x in text for x in ["unfortunately", "we regret", "not moving forward", "after careful consideration"]):
        return "REJECTION"

    # 3. PRIORITY 2: INTERVIEWS / NEXT STEPS
    # Mid-signal words that mean progress.
    if any(x in text for x in ["interview", "next step", "assessment", "calendar invite", "schedule a call"]):
        return "INTERVIEW"

    # 4. PRIORITY 3: APPLICATION CONFIRMATIONS
    # Low-signal words that mean a NEW entry is needed.
    if any(x in text for x in ["your application was sent", "received your application", "thank you for applying", "applied to"]):
        return "APPLICATION_CONFIRMATION"

    # 5. ALL OTHER NOISE
    return "IGNORE"