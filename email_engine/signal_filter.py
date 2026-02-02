# email_engine/signal_filter.py

def is_real_job_email(subject, body, sender):
    text = f"{subject} {body}".lower()

    # ❌ HARD BLOCK LIST (The Junk Filter)
    block = [
        "course", "certificate", "webinar", "expo", "event",
        "training", "bootcamp", "newsletter", "investment", 
        "sip", "mutual fund", "github", "oauth", "security alert",
        "promotion", "offer", "purchase", "reference no"
    ]
    if any(b in text for b in block):
        return False

    # ✅ MUST HAVE BOTH: An Action AND a Job Entity
    job_action = ["application", "applied", "interview", "shortlisted", "rejected", "not moving forward", "next steps"]
    job_entity = ["role", "position", "analyst", "engineer", "researcher", "manager", "developer", "quant"]

    has_action = any(a in text for a in job_action)
    has_entity = any(e in text for e in job_entity)

    return has_action and has_entity