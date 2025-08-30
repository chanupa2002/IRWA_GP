# single_file_document_topic_classifier.py

import requests
from transformers import pipeline

# Initialize zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define candidate topics (you can customize this list)
candidate_topics = [
    "Technology", "Science", "Business", "Health", "Education",
    "Sports", "Politics", "Entertainment", "Environment", "Finance"
]

# Input: list of document URLs
document_links = [
    "https://www.nejm.org/doi/10.1056/NEJMoa1707447",
    "https://pubmed.ncbi.nlm.nih.gov/38238616/",
    # Add up to 10 document links
]

def fetch_document_content(url):
    """Fetch text content from a document URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def classify_document(content):
    """Classify document topic."""
    result = classifier(content, candidate_topics)
    # Return the topic with highest score
    return result['labels'][0]

def main():
    for idx, link in enumerate(document_links, start=1):
        print(f"\nProcessing Document {idx}: {link}")
        content = fetch_document_content(link)
        if content:
            topic = classify_document(content)
            print(f"Document {idx} Topic: {topic}")
        else:
            print(f"Document {idx} Topic: Could not fetch content")

if __name__ == "__main__":
    main()
