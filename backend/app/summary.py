# import requests
# from bs4 import BeautifulSoup
# import google.generativeai as genai
# import os
# from PyPDF2 import PdfReader
# from io import BytesIO
# from dotenv import load_dotenv
# # --- CONFIGURATION ---

# load_dotenv()  # this loads .env into environment variables

# API_KEY = os.getenv("GEMINI_API_KEY")
# if not API_KEY:
#     raise RuntimeError("GEMINI_API_KEY is missing. Set it in environment variables.")
# genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel(model_name="gemini-2.5-flash")  # or gemini-1.5-pro

# # -----------------------------
# # Fetch content
# # -----------------------------
# def fetch_url_content(url: str) -> str:
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         content_type = response.headers.get("Content-Type", "").lower()

#         # ---- PDF Handling ----
#         if url.endswith(".pdf") or "application/pdf" in content_type or "application/octet-stream" in content_type:
#             pdf_file = BytesIO(response.content)
#             pdf_reader = PdfReader(pdf_file)
#             text = []
#             for page in pdf_reader.pages:
#                 page_text = page.extract_text()
#                 if page_text:
#                     text.append(page_text.strip())
#             return "\n".join(text)

#         # ---- HTML Handling ----
#         elif "text/html" in content_type:
#             soup = BeautifulSoup(response.text, "html.parser")

#             # remove unwanted tags
#             for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
#                 tag.extract()

#             collected = []
#             seen = set()

#             # helper to add text if unique & useful
#             def add_text(txt, is_heading=False):
#                 txt = txt.strip()
#                 if txt and txt not in seen:
#                     if is_heading or len(txt) > 30:  # keep short only if heading
#                         collected.append(txt)
#                         seen.add(txt)

#             # headings
#             for level in range(1, 7):
#                 for h in soup.find_all(f"h{level}"):
#                     add_text(h.get_text(" ", strip=True), is_heading=True)

#             # paragraphs
#             for p in soup.find_all("p"):
#                 add_text(p.get_text(" ", strip=True))

#             # list items
#             for li in soup.find_all("li"):
#                 add_text(li.get_text(" ", strip=True))

#             # articles / sections
#             for sec in soup.find_all(["article", "section"]):
#                 add_text(sec.get_text(" ", strip=True))

#             return "\n".join(collected)

#         else:
#             return "Unsupported content type: " + content_type

#     except Exception as e:
#         return f"Error fetching {url}: {e}"


# # -----------------------------
# # Summarization
# # -----------------------------
# def summarize_with_gemini(text: str) -> str:
#     """Send content to Gemini for summarization."""
#     prompt = (
#         "Summarize the following content in a detailed, thorough, and comprehensive manner. "
#         "Include key points, explanations, and context:\n\n"
#         f"{text}"
#     )
#     response = model.generate_content(prompt)
#     return response.text


# def summarize_url(url: str, fetch_only: bool = False) -> str:
#     """Fetch content from URL and optionally summarize it."""
#     print(f"Fetching content from: {url}")
#     content = fetch_url_content(url)
#     print("Fetched content length:", len(content))
#     print("Content preview:", content[:500])

#     if fetch_only:
#         return content

#     # Optional: chunk if too long
#     max_chunk_chars = 5000
#     if len(content) > max_chunk_chars:
#         chunks = [content[i:i+max_chunk_chars] for i in range(0, len(content), max_chunk_chars)]
#         chunk_summaries = [summarize_with_gemini(c) for c in chunks]
#         final_summary = summarize_with_gemini(" ".join(chunk_summaries))
#     else:
#         final_summary = summarize_with_gemini(content)

#     return final_summary



# summary.py
# import requests
# from bs4 import BeautifulSoup
# from PyPDF2 import PdfReader
# from io import BytesIO
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# from transformers import pipeline

# # -----------------------------
# # CONFIGURATION
# # -----------------------------
# load_dotenv()  # Load .env variables

# API_KEY = os.getenv("GEMINI_API_KEY")
# if API_KEY:
#     genai.configure(api_key=API_KEY)
#     gemini_model = genai.GenerativeModel(model_name="gemini-2.5-flash")
# else:
#     gemini_model = None

# # Local transformer summarizer (fallback)
# transformer_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# # -----------------------------
# # FETCH CONTENT
# # -----------------------------
# def fetch_url_content(url: str) -> str:
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         content_type = response.headers.get("Content-Type", "").lower()

#         # PDF handling
#         if url.endswith(".pdf") or "application/pdf" in content_type or "application/octet-stream" in content_type:
#             pdf_file = BytesIO(response.content)
#             pdf_reader = PdfReader(pdf_file)
#             text = [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
#             return "\n".join(text)

#         # HTML handling
#         elif "text/html" in content_type:
#             soup = BeautifulSoup(response.text, "html.parser")
#             for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
#                 tag.extract()
#             collected = []
#             seen = set()
#             def add_text(txt, is_heading=False):
#                 txt = txt.strip()
#                 if txt and txt not in seen:
#                     if is_heading or len(txt) > 10:  # include short meaningful text too
#                         collected.append(txt)
#                         seen.add(txt)
#             # headings
#             for level in range(1, 7):
#                 for h in soup.find_all(f"h{level}"):
#                     add_text(h.get_text(" ", strip=True), is_heading=True)
#             # paragraphs
#             for p in soup.find_all("p"):
#                 add_text(p.get_text(" ", strip=True))
#             # list items
#             for li in soup.find_all("li"):
#                 add_text(li.get_text(" ", strip=True))
#             # articles/sections
#             for sec in soup.find_all(["article", "section"]):
#                 add_text(sec.get_text(" ", strip=True))
#             return "\n".join(collected)

#         else:
#             return f"Unsupported content type: {content_type}"

#     except Exception as e:
#         return f"Error fetching {url}: {e}"

# # -----------------------------
# # SUMMARIZATION
# # -----------------------------
# def summarize_with_gemini(text: str) -> str:
#     """Send content to Gemini for summarization."""
#     if not gemini_model:
#         raise RuntimeError("Gemini API key not configured.")
#     prompt = (
#         "Summarize the following content in a detailed, thorough, and comprehensive manner. "
#         "Include key points, explanations, and context:\n\n"
#         f"{text}"
#     )
#     response = gemini_model.generate_content(prompt)
#     return response.text

# def summarize_with_transformers(text: str, max_chunk_chars=1000) -> str:
#     """Local summarization using transformers pipeline."""
#     chunks = [text[i:i+max_chunk_chars] for i in range(0, len(text), max_chunk_chars)]
#     chunk_summaries = [
#         transformer_summarizer(c, max_length=200, min_length=50, do_sample=False)[0]["summary_text"]
#         for c in chunks
#     ]
#     if len(chunk_summaries) > 1:
#         final_summary = transformer_summarizer(
#             " ".join(chunk_summaries), max_length=300, min_length=100, do_sample=False
#         )[0]["summary_text"]
#     else:
#         final_summary = chunk_summaries[0]
#     return final_summary

# # -----------------------------
# # COMBINED SUMMARIZATION
# # -----------------------------
# def summarize_text(text: str, fallback_to_transformer=True) -> str:
#     """Try Gemini summarization, fallback to transformer if needed or text is too long."""
#     summary = None
#     try:
#         if gemini_model and len(text) < 5000:
#             summary = summarize_with_gemini(text)
#         else:
#             summary = summarize_with_transformers(text)
#     except Exception:
#         if fallback_to_transformer:
#             summary = summarize_with_transformers(text)
#         else:
#             summary = "Summary could not be generated."
#     return summary

# def summarize_url(url: str, fetch_only: bool = False) -> str:
#     """Fetch content from URL and summarize using combined method."""
#     content = fetch_url_content(url)
#     if "403 Client Error" in content or "Error fetching" in content:
#         return "Summary not available: the paper is behind a paywall or inaccessible."
#     if fetch_only:
#         return content
#     return summarize_text(content)


# # summary.py
# import requests
# from bs4 import BeautifulSoup
# from PyPDF2 import PdfReader
# from io import BytesIO
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# from transformers import pipeline

# # -----------------------------
# # CONFIGURATION
# # -----------------------------
# load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")
# if API_KEY:
#     genai.configure(api_key=API_KEY)
#     gemini_model = genai.GenerativeModel(model_name="gemini-2.5-flash")
# else:
#     gemini_model = None

# # Local transformer summarizer (fallback)
# transformer_summarizer = pipeline(
#     "summarization",
#     model="facebook/bart-large-cnn",
#     device=0 if os.environ.get("CUDA_VISIBLE_DEVICES") else -1
# )

# # -----------------------------
# # FETCH CONTENT
# # -----------------------------
# def fetch_url_content(url: str) -> str:
#     """Fetch content from URL or PDF."""
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         content_type = response.headers.get("Content-Type", "").lower()

#         # PDF handling
#         if url.endswith(".pdf") or "application/pdf" in content_type or "application/octet-stream" in content_type:
#             pdf_file = BytesIO(response.content)
#             pdf_reader = PdfReader(pdf_file)
#             # Extract first 5 pages for speed
#             text = [page.extract_text() for i, page in enumerate(pdf_reader.pages) if i < 5 and page.extract_text()]
#             if not text:
#                 return "PDF content empty or not extractable"
#             return "\n".join(text)

#         # HTML handling
#         elif "text/html" in content_type:
#             soup = BeautifulSoup(response.text, "html.parser")
#             for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
#                 tag.extract()
#             collected = []
#             seen = set()
#             def add_text(txt, is_heading=False):
#                 txt = txt.strip()
#                 if txt and txt not in seen:
#                     if is_heading or len(txt) > 10:
#                         collected.append(txt)
#                         seen.add(txt)
#             # headings
#             for level in range(1, 7):
#                 for h in soup.find_all(f"h{level}"):
#                     add_text(h.get_text(" ", strip=True), is_heading=True)
#             # paragraphs
#             for p in soup.find_all("p"):
#                 add_text(p.get_text(" ", strip=True))
#             # list items
#             for li in soup.find_all("li"):
#                 add_text(li.get_text(" ", strip=True))
#             # articles/sections
#             for sec in soup.find_all(["article", "section"]):
#                 add_text(sec.get_text(" ", strip=True))
#             return "\n".join(collected)

#         else:
#             return f"Unsupported content type: {content_type}"

#     except requests.exceptions.HTTPError as e:
#         if e.response.status_code == 403:
#             return "403 Forbidden"
#         return f"HTTP Error: {e}"
#     except Exception as e:
#         return f"Error fetching {url}: {e}"

# # -----------------------------
# # SUMMARIZATION
# # -----------------------------
# def summarize_with_gemini(text: str) -> str:
#     if not gemini_model:
#         raise RuntimeError("Gemini API key not configured.")
#     prompt = (
#         "Summarize the following content in a detailed, thorough, and comprehensive manner. "
#         "Include key points, explanations, and context:\n\n"
#         f"{text}"
#     )
#     response = gemini_model.generate_content(prompt)
#     return response.text

# def summarize_with_transformers(text: str, max_chunk_chars=2000) -> str:
#     chunks = [text[i:i+max_chunk_chars] for i in range(0, len(text), max_chunk_chars)]
#     summaries = [
#         transformer_summarizer(c, max_length=200, min_length=50, do_sample=False)[0]["summary_text"]
#         for c in chunks
#     ]
#     if len(summaries) > 1:
#         final_summary = transformer_summarizer(
#             " ".join(summaries), max_length=300, min_length=100, do_sample=False
#         )[0]["summary_text"]
#     else:
#         final_summary = summaries[0]
#     return final_summary

# def summarize_text(text: str) -> str:
#     try:
#         if gemini_model and len(text) < 5000:
#             return summarize_with_gemini(text)
#         else:
#             return summarize_with_transformers(text)
#     except Exception:
#         return summarize_with_transformers(text)

# def summarize_url(url: str) -> str:
#     content = fetch_url_content(url)
#     if "403 Forbidden" in content or "PDF content empty" in content or "Error fetching" in content:
#         return "Summary not available: the paper is behind a paywall or inaccessible."
#     return summarize_text(content)




# import requests
# from bs4 import BeautifulSoup
# import fitz  # ✅ Fast PyMuPDF for text extraction
# from io import BytesIO
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# from transformers import pipeline
# import asyncio

# # -----------------------------
# # CONFIGURATION
# # -----------------------------
# load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")
# if API_KEY:
#     genai.configure(api_key=API_KEY)
#     gemini_model = genai.GenerativeModel(model_name="gemini-2.5-flash")
# else:
#     gemini_model = None

# # Local transformer summarizer (fallback)
# transformer_summarizer = pipeline(
#     "summarization",
#     model="facebook/bart-large-cnn",
#     device=0 if os.environ.get("CUDA_VISIBLE_DEVICES") else -1
# )

# # -----------------------------
# # FETCH CONTENT
# # -----------------------------
# def fetch_url_content(url: str) -> str:
#     """Fetch content from URL or PDF using PyMuPDF for speed."""
#     try:
#         print(f"Fetching: {url}")
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         content_type = response.headers.get("Content-Type", "").lower()

#         # ✅ PDF handling (fast)
#         if url.endswith(".pdf") or "application/pdf" in content_type:
#             print("Extracting text from PDF...")
#             pdf_data = BytesIO(response.content)
#             text_chunks = []
#             with fitz.open(stream=pdf_data, filetype="pdf") as doc:
#                 for i, page in enumerate(doc):
#                     if i >= 10:  # only first 5 pages
#                         break
#                     page_text = page.get_text("text")
#                     if page_text.strip():
#                         text_chunks.append(page_text)
#             if not text_chunks:
#                 return "PDF content empty or not extractable"
#             print(f"Extracted {len(text_chunks)} pages of text.")
#             return "\n".join(text_chunks)

#         # HTML handling
#         elif "text/html" in content_type:
#             print("Extracting text from HTML...")
#             soup = BeautifulSoup(response.text, "html.parser")
#             for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
#                 tag.extract()
#             collected, seen = [], set()

#             def add_text(txt, is_heading=False):
#                 txt = txt.strip()
#                 if txt and txt not in seen:
#                     if is_heading or len(txt) > 10:
#                         collected.append(txt)
#                         seen.add(txt)

#             for level in range(1, 7):
#                 for h in soup.find_all(f"h{level}"):
#                     add_text(h.get_text(" ", strip=True), is_heading=True)
#             for p in soup.find_all("p"):
#                 add_text(p.get_text(" ", strip=True))
#             for li in soup.find_all("li"):
#                 add_text(li.get_text(" ", strip=True))
#             for sec in soup.find_all(["article", "section"]):
#                 add_text(sec.get_text(" ", strip=True))
#             print(f"Extracted {len(collected)} HTML text blocks.")
#             return "\n".join(collected)

#         else:
#             return f"Unsupported content type: {content_type}"

#     except requests.exceptions.HTTPError as e:
#         if e.response.status_code == 403:
#             return "403 Forbidden"
#         return f"HTTP Error: {e}"
#     except Exception as e:
#         return f"Error fetching {url}: {e}"

# # -----------------------------
# # SUMMARIZATION
# # -----------------------------
# def summarize_with_gemini(text: str) -> str:
#     if not gemini_model:
#         raise RuntimeError("Gemini API key not configured.")
#     prompt = (
#         "Summarize the following content in a detailed and comprehensive manner. "
#         "Include key points, methods, results, and significance. Avoid markdown formatting.\n\n"
#         f"{text}"
#     )
#     print("Sending to Gemini...")
#     response = gemini_model.generate_content(prompt)
#     return response.text


# def summarize_with_transformers(text: str, max_chunk_chars=2000) -> str:
#     chunks = [text[i:i+max_chunk_chars] for i in range(0, len(text), max_chunk_chars)]
#     summaries = [
#         transformer_summarizer(c, max_length=500, min_length=150, do_sample=False)[0]["summary_text"]
#         for c in chunks
#     ]
#     if len(summaries) > 1:
#         final_summary = transformer_summarizer(
#             " ".join(summaries), max_length=700, min_length=200, do_sample=False
#         )[0]["summary_text"]
#     else:
#         final_summary = summaries[0]
#     return final_summary


# async def summarize_text(text: str) -> str:
#     """Summarize text asynchronously with Gemini or Transformers (limit long input)."""
#     text = text[:8000]  # ✅ limit to avoid timeout
#     try:
#         if gemini_model and len(text) < 5000:
#             return await asyncio.to_thread(summarize_with_gemini, text)
#         else:
#             return await asyncio.to_thread(summarize_with_transformers, text)
#     except Exception:
#         return await asyncio.to_thread(summarize_with_transformers, text)


# async def summarize_url(url: str) -> str:
#     """Fetch and summarize content (async-safe)."""
#     content = await asyncio.to_thread(fetch_url_content, url)
#     if "403 Forbidden" in content or "PDF content empty" in content or "Error fetching" in content:
#         return "Summary not available: the paper is behind a paywall or inaccessible."
#     return await summarize_text(content)


import requests
from bs4 import BeautifulSoup
import fitz  # ✅ Fast PyMuPDF for text extraction
from io import BytesIO
import google.generativeai as genai
import os
from dotenv import load_dotenv
from transformers import pipeline
import asyncio
from playwright.sync_api import sync_playwright  # ✅ Option 2: Headless browser

# -----------------------------
# CONFIGURATION
# -----------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    gemini_model = genai.GenerativeModel(model_name="gemini-2.5-flash")
else:
    gemini_model = None

# Local transformer summarizer (fallback)
transformer_summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=0 if os.environ.get("CUDA_VISIBLE_DEVICES") else -1
)

# -----------------------------
# OPTION 2: FETCH USING PLAYWRIGHT
# -----------------------------
def fetch_with_playwright(url: str) -> str:
    """Use Playwright to load JavaScript-rendered pages (Option 2)."""
    try:
        print(f"[Playwright] Launching headless browser for: {url}")
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(20000)
            page.goto(url, wait_until="networkidle")

            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")

        # Clean up irrelevant tags
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
            tag.extract()

        text_blocks = []
        for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "article", "section"]):
            txt = tag.get_text(" ", strip=True)
            if txt and len(txt) > 20:
                text_blocks.append(txt)

        if not text_blocks:
            return "Error: no readable text found even after rendering."

        print(f"[Playwright] Extracted {len(text_blocks)} blocks of text.")
        return "\n".join(text_blocks[:300])  # limit for safety

    except Exception as e:
        return f"[Playwright Error] {e}"

# -----------------------------
# FETCH CONTENT (DEFAULT + PLAYWRIGHT FALLBACK)
# -----------------------------
def fetch_url_content(url: str) -> str:
    """Fetch content from URL or PDF using requests or Playwright."""
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "").lower()

        # ✅ PDF handling (fast)
        if url.endswith(".pdf") or "application/pdf" in content_type:
            print("Extracting text from PDF...")
            pdf_data = BytesIO(response.content)
            text_chunks = []
            with fitz.open(stream=pdf_data, filetype="pdf") as doc:
                for i, page in enumerate(doc):
                    if i >= 10:  # only first 10 pages
                        break
                    page_text = page.get_text("text")
                    if page_text.strip():
                        text_chunks.append(page_text)
            if not text_chunks:
                return "PDF content empty or not extractable"
            print(f"Extracted {len(text_chunks)} pages of text.")
            return "\n".join(text_chunks)

        # ✅ HTML handling
        elif "text/html" in content_type:
            print("Extracting text from HTML...")
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
                tag.extract()

            collected, seen = [], set()

            def add_text(txt, is_heading=False):
                txt = txt.strip()
                if txt and txt not in seen:
                    if is_heading or len(txt) > 10:
                        collected.append(txt)
                        seen.add(txt)

            for level in range(1, 7):
                for h in soup.find_all(f"h{level}"):
                    add_text(h.get_text(" ", strip=True), is_heading=True)
            for tag in soup.find_all(["p", "li", "article", "section"]):
                add_text(tag.get_text(" ", strip=True))

            if not collected:
                print("No static text found, switching to Playwright...")
                return fetch_with_playwright(url)

            print(f"Extracted {len(collected)} HTML text blocks.")
            return "\n".join(collected)

        else:
            return f"Unsupported content type: {content_type}"

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print("403 Forbidden detected, switching to Playwright...")
            return fetch_with_playwright(url)
        return f"HTTP Error: {e}"
    except Exception as e:
        print(f"Requests failed, switching to Playwright: {e}")
        return fetch_with_playwright(url)

# -----------------------------
# SUMMARIZATION
# -----------------------------
def summarize_with_gemini(text: str) -> str:
    if not gemini_model:
        raise RuntimeError("Gemini API key not configured.")
    prompt = (
        "Summarize the following content in a detailed and comprehensive manner. "
        "Include key points, methods, results, and significance. Avoid markdown formatting.\n\n"
        f"{text}"
    )
    print("Sending to Gemini...")
    response = gemini_model.generate_content(prompt)
    return response.text


def summarize_with_transformers(text: str, max_chunk_chars=2000) -> str:
    chunks = [text[i:i + max_chunk_chars] for i in range(0, len(text), max_chunk_chars)]
    summaries = [
        transformer_summarizer(c, max_length=500, min_length=150, do_sample=False)[0]["summary_text"]
        for c in chunks
    ]
    if len(summaries) > 1:
        final_summary = transformer_summarizer(
            " ".join(summaries), max_length=700, min_length=200, do_sample=False
        )[0]["summary_text"]
    else:
        final_summary = summaries[0]
    return final_summary


async def summarize_text(text: str) -> str:
    """Summarize text asynchronously with Gemini or Transformers (limit long input)."""
    text = text[:8000]  # ✅ limit to avoid timeout
    try:
        if gemini_model and len(text) < 5000:
            return await asyncio.to_thread(summarize_with_gemini, text)
        else:
            return await asyncio.to_thread(summarize_with_transformers, text)
    except Exception:
        return await asyncio.to_thread(summarize_with_transformers, text)


async def summarize_url(url: str) -> str:
    """Fetch and summarize content (async-safe)."""
    content = await asyncio.to_thread(fetch_url_content, url)
    if any(err in content for err in ["403 Forbidden", "PDF content empty", "Error fetching", "Playwright Error"]):
        return "Summary not available: the paper is behind a paywall or inaccessible."
    return await summarize_text(content)


