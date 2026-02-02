# Recruiter Response Intelligence System (RRIS)

## 🚀 Overview

Recruiter Response Intelligence System (RRIS) is a **local-first, AI-powered application intelligence system** that ingests recruiter and hiring emails, analyzes full message context, and converts inbox noise into a **clean, auditable job-application intelligence layer**.

Unlike keyword-based trackers, RRIS understands **intent, status changes, reminders, and interview signals** across entire email threads — all while keeping your data **private and local**.

---

## 🧠 Core Capabilities

* 📩 Multi-folder email ingestion (Inbox, Junk, Sent)
* 🧠 Local AI/NLP classification using LLMs
* 🏷️ Accurate company & role extraction from full email bodies
* 🕒 Historical lifecycle tracking (Applied → Viewed → Interview → Rejected)
* 🔄 Deduplication across reminders, forwards, and threads
* 📊 Structured persistence to Google Sheets
* 🔐 Security-first design (local token cache, secrets excluded from Git)

---

## 🧰 Tech Stack

* **Python 3.10+** – Core system logic
* **Microsoft Graph API** – Outlook email ingestion
* **Google Sheets API** – Structured data persistence
* **Ollama (Llama 3.2+)** – Local LLM inference (privacy-first)
* **BeautifulSoup4** – HTML email parsing
* **Regex + Rule Engines** – Deterministic fallbacks for accuracy

---

## ⚙️ Prerequisites

Before running RRIS, ensure the following:

* 🧠 **Ollama must be installed and running locally**

  * Download: [https://ollama.ai](https://ollama.ai)
  * Example:

    ```bash
    ollama pull llama3.2
    ```
* 🔑 Microsoft Outlook account with Graph API access
* 📊 Google Cloud project with Sheets API enabled

> ⚠️ Without Ollama running locally, AI classification features will not function.

---

## 🏗️ Architecture Overview

RRIS follows a **modular, pipeline-driven architecture**:

1. Authentication Layer (Outlook + Google)
2. Email Fetch Engine (full-context ingestion)
3. Processing Pipeline (cleaning & normalization)
4. AI Classification Layer (local LLM inference)
5. Signal Filter (noise removal)
6. State Manager (application lifecycle tracking)
7. Persistence Layer (Google Sheets / datastore)

This design enables **safe iteration, model upgrades, and new data backends** without breaking the system.

---

## 📁 Project Structure

```
PROJECT ROOT
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── check_files.py
├── check_integrity.py
├── export_project.py
├── FULL_PROJECT_CODE.txt
├── token_cache.json
│
├── auth/
│   ├── outlook_auth.py
│   ├── gsheet_auth.py
│   └── __init__.py
│
├── email_engine/
│   ├── fetch_emails.py
│   ├── extractor.py
│   ├── classifier.py
│   ├── linkedin_parser.py
│   ├── processor.py
│   ├── signal_filter.py
│   ├── state_manager.py
│   └── __init__.py
│
├── config/
│   ├── outlook_config.py
│   ├── gsheet_config.py
│   ├── credentials.json
│   └── token_cache.bin
│
└── database/
    ├── sheet_manager.py
    └── __init__.py
```

---

## ▶️ Running the System

```bash
pip install -r requirements.txt
python main.py
```

---

## 🔐 Security Notes

* Sensitive tokens are cached locally and **must never be committed**
* `.gitignore` excludes token and credential artifacts
* GitHub push protection is intentionally respected

---

## 📜 License

This project is released under the **MIT License**.

---

## 🧠 Philosophy

RRIS is designed as an **application intelligence system**, not a simple tracker. The goal is to give candidates the same visibility and rigor that enterprises use internally — **signals, timelines, and truth over guesswork**.

Author: Hemant Verma
Focus: AI • Quant • Risk • Application Intelligence