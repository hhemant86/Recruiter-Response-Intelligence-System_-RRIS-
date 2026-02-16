# email_engine/signal_filter.py

def is_real_job_email(subject, body, sender):
    """
    RRIS Layer 1: The Iron Curtain (LinkedIn Optimized)
    Refines 1,800+ emails into ~100 high-value career signals.
    """
    sender = sender.lower()
    subject = subject.lower()
    
    # 1. 🛠️ Extract body content safely from Microsoft dictionary structure
    content = body.get('content', '').lower() if isinstance(body, dict) else str(body).lower()

    # 2. 🚫 THE INSTANT KILL LIST (Non-Job Domains)
    trash_domains = [
        'bigbasket.com', 'etihad.com', 'ramada.com', 'microsoft.com', 
        'news.linkedin.com', 'notifications@github.com', 'tradingview.com',
        'apple.com', 'amazon.in', 'swiggy.com', 'zomato.com', 'bank', 
        'policybazaar', 'titlestaring', 'jiomart', 'healthians', 'e.linkedin.com',
        'updates.linkedin.com', 'perplex','quora', 'twitter',
        'newsletter.quantinsti.com', 'mail.insead.edu' # Added these
    ]
    if any(domain in sender for domain in trash_domains):
        return False

    # 3. 🚫 THE NOISE SUBJECT KILLER (Marketing & Alerts)
    noise_subjects = [
        'extraordinary general meeting', 'room reservation', 'handpicked jobs',
        'verify your email', 'new device registration', 'posts got', 
        'impressions last week', 'handbook to', 'valentine', 'sale',
        'legal notice', 'newsletter', 'extra saving tips', 'verification code',
        'login link', 'invite to masterclass', 'seasons greetings', 'jobs for you',
        'daily digest', 'weekly digest', 'recommended jobs', 'new jobs' # Added these
    ]
    if any(ns in subject for ns in noise_subjects):
        return False

    # 4. ✅ THE "HIGH-VALUE" GATEKEEPER (LinkedIn Status Support)
    # These signals specifically target the candidacy lifecycle.
    job_signals = [
        'application', 'interview', 'rejected', 'moving forward', 
        'assessment', 'received your', 'shortlisted', 'quant', 'role',
        'viewed your application', 'viewed by', 'hiring', 'resume', 
        'not moving forward', 'status', 'candidate'
    ]
    
    # Check Subject first (highest priority)
    if any(sig in subject for sig in job_signals):
        return True
        
    # Check the "Hook" of the email (First 700 chars)
    # This catches LinkedIn's "Your application was viewed by..." and "Company is not moving forward"
    if any(sig in content[:700] for sig in job_signals):
        return True

    return False