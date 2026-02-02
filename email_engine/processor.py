# email_engine/processor.py
import requests
import json
from bs4 import BeautifulSoup

def analyze_job_email_llm(subject, body_data, sender):
    """Uses Local Ollama with full-body context and HTML cleaning."""
    
    # FIX: Handle cases where body_data is a string OR a dictionary
    if isinstance(body_data, dict):
        html_content = body_data.get('content', '')
    else:
        html_content = str(body_data)

    # Clean HTML to plain text
    soup = BeautifulSoup(html_content, 'html.parser')
    plain_text = soup.get_text(separator=' ', strip=True)

    url = "http://localhost:11434/api/generate"
    
    # email_engine/processor.py
# ... (BeautifulSoup logic remains the same) ...

    prompt = f"""
    You are a professional Job Tracker. Your goal is to find the ACTUAL HIRING COMPANY.
    
    CRITICAL RULES:
    1. COMPANY: If the email is from LinkedIn/Naukri/Indeed, IGNORE them. Look deep in the text for the employer (e.g., CoinDCX, RGG Capital, Alpha Access). 
    2. REJECTION: If you see "Unfortunately", "will not be moving forward", or "decided to move on", Status is "Rejected".
    3. ROLE: If the role is missing, use "Quantitative Analyst".

    Subject: {subject}
    Email Body: {plain_text[:2500]} 

    Return ONLY JSON:
    {{"company": "REAL_EMPLOYER_NAME", "role": "TITLE", "status": "Applied/Interview/Rejected"}}
    """

    
    payload = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False,
        "format": "json" 
    }
    
    try:
        response = requests.post(url, json=payload, timeout=90)
        response.raise_for_status()
        return json.loads(response.json()['response'])
    except Exception as e:
        print(f"⚠️ Local AI Error: {e}")
        return {"company": "Unknown", "role": "Position", "status": "Applied"}