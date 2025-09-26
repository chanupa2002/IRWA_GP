# topic_classifier.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- CONFIG ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Set it in environment variables.")
genai.configure(api_key=API_KEY)

MODEL = "gemini-2.5-flash"  # You can change to gemini-pro if needed

def classify_topic(text: str) -> str:
    """
    Classifies the topic of a research paper based on summary or title.
    Returns a string label like 'Computer Science - NLP' or 'Biology - Genetics'.
    """

    if not text or text.strip() == "":
        return "Unknown"

    prompt = f"""
    You are a topic classifier for academic research papers.
    Given the following text (which may be a summary or title), classify the paper into
    one of the major academic disciplines and a subfield if possible.

    Example outputs:
    - "Computer Science - Natural Language Processing"
    - "Physics - Quantum Mechanics"
    - "Biology - Genetics"
    - "Medicine - Oncology"
    - "Economics - Development Economics"

    Text: {text}

    Return only the classification, no explanation.
    """

    try:
        response = genai.GenerativeModel(MODEL).generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error classifying topic: {str(e)}"
