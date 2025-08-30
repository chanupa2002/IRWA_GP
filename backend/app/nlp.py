# nlp.py
import spacy
import os

# load model once (fast to reuse)
# If you want a bigger model for more accurate lemmatization you can change it later
_MODEL = None

def load_model():
    global _MODEL
    if _MODEL is None:
        # set environment variable or fallback to en_core_web_sm
        _MODEL = spacy.load(os.environ.get("SPACY_MODEL", "en_core_web_sm"))
    return _MODEL

def normalize_and_tokenize(text, min_len=2, dedup=True):
    """
    Input: raw text string
    Output: list of normalized terms (lemmatized, lowercased, alpha-only, stopwords removed)
    """
    nlp = load_model()
    doc = nlp(text)
    terms = []
    for token in doc:
        # keep only alphabetic tokens, not punctuation, not whitespace, not stopwords
        if token.is_alpha and not token.is_stop:
            lemma = token.lemma_.lower().strip()
            if len(lemma) >= min_len:
                terms.append(lemma)
    if dedup:
        # preserve order but unique
        seen = set()
        uniq = []
        for t in terms:
            if t not in seen:
                seen.add(t)
                uniq.append(t)
        return uniq
    return terms
