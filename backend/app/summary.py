import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

# --- CONFIGURATION ---
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDRys2RG8W6kcWf2TubzweSk2yO-Z2B4Ks")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro

def fetch_url_content(url: str) -> str:
    """Fetch text content from a webpage or PDF."""
    response = requests.get(url)
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "")

    # PDF
    if "application/pdf" in content_type:
        import PyPDF2
        from io import BytesIO

        reader = PyPDF2.PdfReader(BytesIO(response.content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    # HTML
    elif "text/html" in content_type:
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()
        return " ".join(p.get_text(separator=" ", strip=True) for p in soup.find_all("p"))

    # Plain text fallback
    else:
        return response.text

def summarize_with_gemini(text: str) -> str:
    """Send content to Gemini for summarization."""
    prompt = (
        f"Summarize the following content in a detailed, thorough, and comprehensive manner. "
        f"Include key points, explanations, and context:\n\n{text}"
    )
    response = model.generate_content(prompt)
    return response.text

def summarize_url(url: str, fetch_only: bool = False) -> str:
    """Fetch content from URL and optionally summarize it."""
    print(f"Fetching content from: {url}")
    content = fetch_url_content(url)
    print("Fetched content length:", len(content))
    print("Content preview:", content[:500])

    if fetch_only:
        return content

    # Optional: chunk if too long
    max_chunk_chars = 10000
    if len(content) > max_chunk_chars:
        chunks = [content[i:i+max_chunk_chars] for i in range(0, len(content), max_chunk_chars)]
        chunk_summaries = [summarize_with_gemini(c) for c in chunks]
        final_summary = summarize_with_gemini(" ".join(chunk_summaries))
    else:
        final_summary = summarize_with_gemini(content)
    #return final summary 
    return final_summary

