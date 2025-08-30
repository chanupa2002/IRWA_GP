import requests

def get_text_from_url(url):
    response = requests.get(url)
    content_type = response.headers.get('Content-Type', '')

    # PDF
    if 'application/pdf' in content_type:
        import PyPDF2
        from io import BytesIO

        reader = PyPDF2.PdfReader(BytesIO(response.content))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    # HTML
    elif 'text/html' in content_type:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get all paragraph text
        return " ".join(p.text for p in soup.find_all('p'))

    # Plain text
    else:
        return response.text



from transformers import pipeline

summarizer = pipeline("summarization")

def summarize_text(text, max_length=150, min_length=50):
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def chunk_text(text, max_chars=1000):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
if __name__ == "__main__":
    url = "https://arxiv.org/pdf/2305.15465.pdf"

    paper_text = get_text_from_url(url)

    # Optional: break into chunks if long
    chunks = chunk_text(paper_text, 1000)
    chunk_summaries = [summarize_text(c) for c in chunks]
    final_summary = summarize_text(" ".join(chunk_summaries))

    print("\n-----SUMMARY-----\n")
    print(final_summary)
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

# --- CONFIGURATION ---
# Set your Gemini API Key (replace with your actual key or export it as ENV variable)
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDRys2RG8W6kcWf2TubzweSk2yO-Z2B4Ks")

# Initialize Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro

def fetch_url_content(url: str) -> str:
    """Fetch text content from a webpage."""
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script and style tags
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator=" ", strip=True)
    return text[:12000]  # limit to avoid token overflow

def summarize_with_gemini(text: str) -> str:
    """Send content to Gemini for summarization."""
    prompt = f"Summarize the following webpage content clearly and concisely:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

def main():
    url = "https://edition.cnn.com/2024/08/29/tech/apple-iphone-ai-update"  # Example test URL
    print(f"Fetching content from: {url}\n")

    content = fetch_url_content(url)
    print("Content fetched. Sending to Gemini...\n")

    summary = summarize_with_gemini(content)
    print("=== SUMMARY ===\n")
    print(summary)

if __name__ == "__main__":
    main()


