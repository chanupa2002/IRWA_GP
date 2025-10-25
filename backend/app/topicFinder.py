import os
import re
import numpy as np
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from dotenv import load_dotenv

# Download NLTK resources (only if missing)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

# --- Load API Key ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Set it in environment variables.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.5-flash")  


def preprocess_text(text: str) -> list[str]:
    """Tokenize, normalize, remove stopwords, stemming, lemmatization."""
    tokens = word_tokenize(text.lower())
    tokens = [re.sub(r"[^a-z]", "", t) for t in tokens if t]
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stop_words]

    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    terms = [lemmatizer.lemmatize(stemmer.stem(t)) for t in tokens]

    return terms


def get_candidate_topics(terms: list[str]) -> list[str]:
    """Ask Gemini to suggest 20 research topics based on terms."""
    prompt = (
        "You are an AI research assistant. Based on the following key terms, "
        "suggest 20 specific, unique, and suitable academic research topics. "
        "Do not provide explanations, only a numbered list of topics.\n\n"
        f"Terms: {', '.join(terms)}"
    )

    response = model.generate_content(prompt)
    raw_text = response.text or ""

    topics = [line.strip("0123456789. ") for line in raw_text.split("\n") if line.strip()]
    topics = [t for t in topics if len(t) > 3]
    return topics[:20]


def rank_topics(terms: list[str], topics: list[str], top_n: int = 10) -> list[str]:
    """Rank topics using cosine similarity between terms and topic strings."""
    documents = [" ".join(terms)] + topics
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    ranked_indices = similarity_scores.argsort()[::-1][:top_n]
    return [topics[i] for i in ranked_indices]


def generate_research_topics(paragraph: str) -> list[str]:
    """Main agent: process paragraph → get Gemini topics → rank → return top 10."""
    terms = preprocess_text(paragraph)
    if not terms:
        return ["No valid terms extracted from input."]

    candidate_topics = get_candidate_topics(terms)
    if not candidate_topics:
        return ["Gemini did not return valid topics."]

    return rank_topics(terms, candidate_topics, top_n=10)