# 🧠 AI Study Tutor Agent

A single agent application built with CrewAI, Groq (GPT-OSS-120B), and Streamlit.

## What it does
- Explains study topics
- Generates quiz questions
- Finds learning resources
- Extracts text from PDFs

## Tech Stack
- CrewAI (agent framework)
- Groq (LLM inference)
- Streamlit (UI)
- GPT-OSS-120B (model)

## How to run locally
1. Clone the repo
2. `pip install -r requirements.txt`
3. Create `.streamlit/secrets.toml` with `GROQ_API_KEY = "gsk_..."`
4. `streamlit run app.py`

## Live Demo
Deployed on Streamlit Cloud.
