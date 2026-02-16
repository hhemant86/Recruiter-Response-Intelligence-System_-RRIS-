# Recruiter Response Intelligence System (RRIS)

## 🚀 Overview

Recruiter Response Intelligence System (RRIS) is a **local-first, AI-powered application intelligence system** that transforms unstructured recruiter and ATS emails into a **structured, auditable hiring intelligence pipeline**.

Instead of treating job search as a black box, RRIS models it as a **signal extraction and state-transition problem** — converting inbox noise into actionable insights such as interview momentum, stale leads, and conversion efficiency.

RRIS is designed for **privacy, resilience, and decision quality**, operating fully on local infrastructure with optional cloud APIs for ingestion and persistence.

---

## 🎯 Why RRIS Exists

Modern job searches generate:
- Noisy recruiter emails
- Repeated reminders and threads
- Ambiguous ATS status updates
- Hidden interview signals

RRIS solves this by:
- Tracking **true application states**, not keywords
- Detecting **Applied → Viewed → Interview → Rejected** transitions
- Measuring **ATS pass rate, interview conversion, and momentum**
- Prioritizing **follow-ups and interview preparation**

This system treats job search with the same rigor used in **quantitative risk, trading pipelines, and enterprise analytics**.

---

## 🧠 Core Capabilities

- 📩 Multi-folder email ingestion (Inbox, Junk, Sent)
- 🧠 Local-first AI/NLP classification using LLMs
- 🏷️ Company, role, and intent extraction from full email context
- 🔁 Robust deduplication across reminders, forwards, and threads
- 🔄 Application lifecycle state management
- 📊 Executive dashboard with hiring KPIs
- ⚠️ Stale lead & ghosting risk detection
- 🔄 Graceful fallback when upstream LLM APIs are rate-limited
- 🔐 Security-first design (local tokens, secrets excluded from Git)

---

## 📊 Executive Intelligence Outputs

RRIS automatically computes:

- Total application pipeline size
- ATS pass / resume view rate
- Interview conversion rate
- Active interview tracks
- Recent recruiter activity
- Stale / ghosted applications
- Momentum-based strategic recommendations

These metrics allow candidates to **optimize decisions**, not guess outcomes.

---

## 🧰 Tech Stack

- **Python 3.10+** – Core system & orchestration
- **Microsoft Graph API** – Outlook email ingestion
- **Google Sheets API** – Structured persistence & reporting
- **Ollama (Llama 3.2+)** – Local LLM inference (privacy-first)
- **Optional Cloud LLMs (Groq)** – With automatic rate-limit fallback
- **BeautifulSoup4** – HTML email parsing
- **Regex & Rule Engines** – Deterministic safety nets
- **State Machines** – Application lifecycle tracking

---

## ⚙️ Prerequisites

Before running RRIS, ensure:

### 🧠 Local LLM
- **Ollama must be installed and running**
  - Download: https://ollama.ai
  - Example:
    ```bash
    ollama pull llama3.2
    ```

> ⚠️ AI classification features require Ollama to be running locally.

### 🔑 APIs
- Microsoft Outlook account with Graph API access
- Google Cloud project with Sheets API enabled

---

## 🏗️ Architecture Overview

RRIS follows a **modular, fault-tolerant pipeline architecture**:

1. **Authentication Layer** – Outlook & Google APIs
2. **Email Fetch Engine** – Full-thread ingestion
3. **Processing Pipeline** – Cleaning & normalization
4. **AI Classification Layer** – Local LLM inference
5. **Signal Filter** – Noise suppression
6. **State Manager** – Lifecycle & transitions
7. **Persistence Layer** – Sheets / datastore
8. **Analytics Dashboard** – Decision intelligence

The system is intentionally designed to **degrade gracefully**, ensuring no data loss during API failures or rate limits.

---

## 📁 Project Structure

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
│ ├── outlook_auth.py
│ ├── gsheet_auth.py
│ └── init.py
│
├── email_engine/
│ ├── fetch_emails.py
│ ├── extractor.py
│ ├── classifier.py
│ ├── linkedin_parser.py
│ ├── processor.py
│ ├── signal_filter.py
│ ├── state_manager.py
│ └── init.py
│
├── config/
│ ├── outlook_config.py
│ ├── gsheet_config.py
│ ├── credentials.json
│ └── token_cache.bin
│
└── database/
├── sheet_manager.py
└── init.py


---

## ▶️ Running the System

```bash
pip install -r requirements.txt
python main.py


python -m analytics.dashboard


🔐 Security & Privacy

All AI inference runs locally by default

Tokens and credentials are never committed

.gitignore enforces secret hygiene

Designed to comply with GitHub push protection

🛣️ Future Roadmap

Multi-inbox support (Gmail, Proton)

Survival analysis & time-to-interview modeling

Interview outcome prediction

Resume–JD semantic alignment scoring

Recruiter response latency analytics

SaaS-mode (opt-in, privacy-preserving)

📜 License

This project is released under the MIT License.

🧠 Philosophy

RRIS treats job search as an intelligence problem, not a numbers game.

The goal is simple:

Replace guesswork with signals, noise with structure, and anxiety with clarity.

Author: Hemant Verma
Focus: Quantitative Analysis • Risk Systems • AI • Application Intelligence