import os
import PyPDF2
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# Download NLTK resources (only first run)
nltk.download("punkt")
nltk.download("punkt_tab")   # <-- add this line
nltk.download("stopwords")
nltk.download("wordnet")

# Initialize tools
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def preprocess_text(text):
    """Clean and preprocess text with lemmatization and stemming."""
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]  # Lemmatization
    tokens = [stemmer.stem(t) for t in tokens]          # Stemming
    return " ".join(tokens)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# Example training data (replace with your dataset)
train_data = [
    ("This study investigates deep learning models for image recognition.", "Computer Science"),
    ("We analyze Shakespeare’s influence on modern English literature.", "Literature"),
    ("A new algorithm for protein folding using quantum computing.", "Biology"),
    ("Exploring feminist perspectives in contemporary poetry.", "Literature")
]

X_train = [preprocess_text(text) for text, _ in train_data]
y_train = [label for _, label in train_data]

# Build model pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=1000))
])

# Train
model.fit(X_train, y_train)

# Save model for reuse
joblib.dump(model, "topic_classifier.pkl")

# -------------------- #
# Example: Classify PDF
# -------------------- #
pdf_path = "example_paper.pdf"  # your input PDF file
abstract_text = extract_text_from_pdf(pdf_path)
clean_text = preprocess_text(abstract_text)

# Load trained model
model = joblib.load("topic_classifier.pkl")
predicted_topic = model.predict([clean_text])[0]

print(f"Predicted topic: {predicted_topic}")
