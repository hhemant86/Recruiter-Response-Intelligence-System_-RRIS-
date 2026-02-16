import os
import json
import requests
import time
from groq import Groq
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

# --- Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"
PRIMARY_GROQ_MODEL = "llama-3.1-8b-instant" 

client = Groq(api_key=GROQ_API_KEY)

def clean_html(html):
    if html is None: return ""
    markup = str(html)
    try:
        soup = BeautifulSoup(markup, "html.parser")
        for script_or_style in soup(["script", "style", "meta", "link"]):
            script_or_style.decompose()
        return soup.get_text(separator=' ', strip=True)[:5000]
    except Exception as e:
        print(f"⚠️ Cleaning Error: {e}")
        return markup[:5000]

def analyze_with_groq(prompt):
    if not GROQ_API_KEY: return None
    try:
        completion = client.chat.completions.create(
            model=PRIMARY_GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return completion.choices[0].message.content
    except Exception as e:
        if "429" in str(e):
            print("⏳ Groq Rate Limit Hit (429).")
        else:
            print(f"⚠️ Groq Error: {e}")
        return None

def analyze_with_ollama(prompt):
    print("🔄 Fallback: Processing with local Ollama...")
    payload = {
        "model": OLLAMA_MODEL, 
        "prompt": prompt + "\nReturn JSON ONLY. If multiple items found, return a list containing one object.", 
        "stream": False, 
        "format": "json"
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        return response.json().get("response")
    except Exception as e:
        print(f"❌ Ollama Error: {e}")
        return None

def analyze_job_email_llm(subject, email_body, sender):
    """
    Polished Orchestration: Handles list returns and rate-limit fallbacks.
    """
    clean_text = clean_html(email_body)
    
    prompt = f"""
    System: Act as a Career Intelligence Architect. Extract job data.
    Return ONLY a JSON object (not a list) with these keys: 
    "company", "role", "status", "reasoning", "is_interview".

    Sender: {sender}
    Subject: {subject}
    Body: {clean_text}

    Valid Statuses: Applied, Viewed, Interview, Rejected, Noise.
    """

    # 1. Attempt Groq, then Fallback to Ollama
    raw_result = analyze_with_groq(prompt)
    if not raw_result:
        raw_result = analyze_with_ollama(prompt)

    if raw_result:
        try:
            # 2. Extract and Parse JSON
            clean_json = raw_result.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            
            # --- THE LIST FIX ---
            if isinstance(data, list):
                data = data[0] if len(data) > 0 else {}

            # --- ROBUST FLATTENING ---
            def flatten(value):
                if isinstance(value, list):
                    return ", ".join(map(str, value))
                return str(value) if value is not None else ""

            company = flatten(data.get("company", "Unknown"))
            role = flatten(data.get("role", "Not specified"))
            status = flatten(data.get("status", "Noise"))
            reasoning = flatten(data.get("reasoning", "Processed"))
            is_int = data.get("is_interview", False)

            # 3. Dynamic Interview Logic
            if is_int is True or "interview" in status.lower():
                status = "Interview"
                if "🔥 PREP" not in reasoning:
                    reasoning = f"🔥 PREP: {reasoning}"

            return {
                "company": company,
                "role": role,
                "status": status,
                "reasoning": reasoning
            }
        except Exception as e:
            print(f"⚠️ JSON Parse Error: {e} | Content: {raw_result[:50]}...")

    return {"company": "Unknown", "role": "Unknown", "status": "Noise", "reasoning": "Extraction Failed"}