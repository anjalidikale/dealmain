# ============================================================
# FILE: triage_ai.py
# ROLE: Data Analyst (DA)
# PURPOSE: Sends patient data to Groq AI and gets triage result.
# NOTE: This file is NOT changed from Day 10.
# ============================================================
 
from groq import Groq
from dotenv import load_dotenv
import os
 
# Load API key from .env file
load_dotenv()
 
# The Groq model we use. This one is free and works on student accounts.
GROQ_MODEL = "openai/gpt-oss-20b"
 
 
def build_prompt(patient):
    """
    Takes patient dict from database and builds a text prompt for AI.
    The prompt tells the AI what the patient symptoms are.
    """
    return f"""
You are a hospital triage nurse. Classify this patient urgency level.
 
Patient Name: {patient["name"]}
Age: {patient["age"]}
Gender: {patient["gender"]}
patient["symptoms"]
Pain Level: {patient["pain_level"]} out of 10
Temperature: {patient["temperature"]} Celsius
Blood Pressure: {patient["systolic_bp"]}/{patient["diastolic_bp"]}
Heart Rate: {patient["heart_rate"]} bpm
 
Give:
1. Triage Category: (Immediate / Urgent / Semi-Urgent / Non-Urgent)
2. Reason: (one sentence)
3. Recommended Action: (what to do right now)
"""
 
 
def run_triage(patient):
    """
    Sends patient data to Groq AI.
    Returns the AI response as a string.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
    prompt = build_prompt(patient)
 
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,    # Low temperature = more predictable, clinical responses
        max_tokens=500,     # Keep responses short
    )
 
    # Extract the AI text from the response object
    return response.choices[0].message.content
