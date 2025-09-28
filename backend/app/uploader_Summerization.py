import os
import re
import fitz  # PyMuPDF for text extraction
import numpy as np
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from dotenv import load_dotenv

# --- Setup NLTK ---
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

# --- Load API Key ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Set it in environment variables.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.5-flash")


# Step 1: Extract text from PDF
def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from a text-based PDF using PyMuPDF (no OCR)."""
    text_chunks = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            page_text = page.get_text("text")
            if page_text.strip():
                text_chunks.append(page_text)
    return "\n".join(text_chunks)


# Step 2: Preprocessing
def preprocess_text(text: str) -> list[str]:
    """Tokenize, normalize, stemming, lemmatization."""
    tokens = word_tokenize(text.lower())
    tokens = [re.sub(r"[^a-z]", "", t) for t in tokens if t.isalpha()]
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stop_words]

    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    terms = [lemmatizer.lemmatize(stemmer.stem(t)) for t in tokens]
    return terms


def select_top_terms(terms: list[str], top_n: int = 100) -> list[str]:
    """Use TF-IDF to select most important terms."""
    if not terms:
        return []

    text = " ".join(terms)
    vectorizer = TfidfVectorizer(max_features=top_n)
    tfidf_matrix = vectorizer.fit_transform([text])
    return list(vectorizer.get_feature_names_out())


def summarize_pdf_terms(terms: list[str]) -> str:
    """Send terms to Gemini and get a summary of research paper."""
    prompt = (
        "You are an academic assistant. Based on the following extracted key terms "
        "from a research paper, write a detailed summary of the paper. "
        "Highlight the research background, methods, findings, and significance.\n\n"
        f"Terms: {', '.join(terms)}"
    )
    response = model.generate_content(prompt)
    return response.text


def summarize_pdf(pdf_path: str) -> str:
    """Main agent: extract → preprocess → top terms → Gemini summary."""
    raw_text = extract_pdf_text(pdf_path)
    if not raw_text.strip():
        return "No text could be extracted from the PDF (might be scanned image-based)."

    terms = preprocess_text(raw_text)
    top_terms = select_top_terms(terms, top_n=100)
    if not top_terms:
        return "No valid terms extracted from the PDF."

    return summarize_pdf_terms(top_terms)
