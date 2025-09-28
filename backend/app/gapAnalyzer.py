import os
import fitz  # PyMuPDF
from transformers import pipeline
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()

# -----------------------------
# STEP 1: Extract text from PDF
# -----------------------------
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

# -----------------------------
# STEP 2: Extract relevant sections
# -----------------------------
def extract_relevant_sections(text):
    sections = {}
    lowered = text.lower()

    def get_section(start_keyword, end_keywords):
        start_idx = lowered.find(start_keyword)
        if start_idx == -1:
            return ""
        end_idx = len(text)
        for ek in end_keywords:
            pos = lowered.find(ek, start_idx + len(start_keyword))
            if pos != -1 and pos < end_idx:
                end_idx = pos
        return text[start_idx:end_idx].strip()

    sections["abstract"] = get_section("abstract", ["introduction", "1. introduction"])
    sections["introduction"] = get_section("introduction", ["method", "approach", "related work"])
    sections["conclusion"] = get_section("conclusion", ["references", "acknowledgment", "acknowledgement"])
    return sections

# -----------------------------
# STEP 3: Summarize with HuggingFace
# -----------------------------
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_len=100):
    if not text.strip():
        return ""
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=max_len, min_length=50, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    return " ".join(summaries)

# -----------------------------
# STEP 4: Analyze gaps with Gemini
# -----------------------------
def analyze_gaps(paper_summaries):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = """
You are a research assistant. Below are summaries of research papers in the same domain.
Identify the research gaps across them.

Provide a comparative gap analysis highlighting:
1. Common areas
2. Unique contributions
3. Gaps not addressed
4. Possible future research directions
"""

    for i, summary in enumerate(paper_summaries, start=1):
        prompt += f"\n\nPaper {i}: {summary}"

    response = model.generate_content(prompt)
    return response.text

# -----------------------------
# STEP 5: Restructure Gemini output
# -----------------------------
def restructure_gap_analysis(raw_output):
    result = {
        "common_areas": [],
        "unique_contributions": {},
        "gaps": [],
        "future_research_directions": []
    }

    lines = raw_output.split("\n")
    current_section = None
    current_paper = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match headings more flexibly
        if re.search(r"common\s+areas", line, re.I):
            current_section = "common_areas"
            continue
        elif re.search(r"unique\s+contributions", line, re.I):
            current_section = "unique_contributions"
            continue
        elif re.search(r"gaps", line, re.I):
            current_section = "gaps"
            continue
        elif re.search(r"future\s+research\s+directions", line, re.I):
            current_section = "future_research_directions"
            continue

        # Handle unique contributions per paper
        if current_section == "unique_contributions":
            paper_match = re.match(r"\*+\s*Paper\s*\d", line)
            if paper_match:
                current_paper = line
                result["unique_contributions"][current_paper] = []
            elif current_paper:
                result["unique_contributions"][current_paper].append(line)
            continue

        # Append lines to other sections
        if current_section in ["common_areas", "gaps", "future_research_directions"]:
            result[current_section].append(line)

    return result

# -----------------------------
# STEP 6: Main pipeline
# -----------------------------
def run_gap_analysis(pdf_paths):
    summaries = []
    for path in pdf_paths:
        text = extract_text_from_pdf(path)
        sections = extract_relevant_sections(text)
        combined_text = " ".join(sections.values())
        summary = summarize_text(combined_text)
        summaries.append(summary)

    raw_analysis = analyze_gaps(summaries)
    print(raw_analysis)
    structured_json = restructure_gap_analysis(raw_analysis)
    return structured_json
