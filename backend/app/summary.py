import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from io import BytesIO
from dotenv import load_dotenv
# --- CONFIGURATION ---

load_dotenv()  # this loads .env into environment variables

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Set it in environment variables.")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.5-flash")  # or gemini-1.5-pro

# -----------------------------
# Fetch content
# -----------------------------
def fetch_url_content(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "").lower()

        # ---- PDF Handling ----
        if url.endswith(".pdf") or "application/pdf" in content_type or "application/octet-stream" in content_type:
            pdf_file = BytesIO(response.content)
            pdf_reader = PdfReader(pdf_file)
            text = []
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text.strip())
            return "\n".join(text)

        # ---- HTML Handling ----
        elif "text/html" in content_type:
            soup = BeautifulSoup(response.text, "html.parser")

            # remove unwanted tags
            for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
                tag.extract()

            collected = []
            seen = set()

            # helper to add text if unique & useful
            def add_text(txt, is_heading=False):
                txt = txt.strip()
                if txt and txt not in seen:
                    if is_heading or len(txt) > 30:  # keep short only if heading
                        collected.append(txt)
                        seen.add(txt)

            # headings
            for level in range(1, 7):
                for h in soup.find_all(f"h{level}"):
                    add_text(h.get_text(" ", strip=True), is_heading=True)

            # paragraphs
            for p in soup.find_all("p"):
                add_text(p.get_text(" ", strip=True))

            # list items
            for li in soup.find_all("li"):
                add_text(li.get_text(" ", strip=True))

            # articles / sections
            for sec in soup.find_all(["article", "section"]):
                add_text(sec.get_text(" ", strip=True))

            return "\n".join(collected)

        else:
            return "Unsupported content type: " + content_type

    except Exception as e:
        return f"Error fetching {url}: {e}"


# -----------------------------
# Summarization
# -----------------------------
def summarize_with_gemini(text: str) -> str:
    """Send content to Gemini for summarization."""
    prompt = (
        "Summarize the following content in a detailed, thorough, and comprehensive manner. "
        "Include key points, explanations, and context:\n\n"
        f"{text}"
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

    return final_summary
