from fastapi import FastAPI, Query, HTTPException,UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .nlp import normalize_and_tokenize
from .semantic import search_semantic_scholar
from .ranking import rank_papers
from .summary import summarize_with_gemini,summarize_url
from pydantic import BaseModel
from typing import List, Optional
import smtplib
from email.mime.text import MIMEText
import re
from fastapi import Depends

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi import Request
from .topic_classifier import classify_topic
from .gapAnalyzer import run_gap_analysis
import os


app = FastAPI(title="PaperForge Backend")




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please wait a few minutes before trying again."},
    )


SAFE_QUERY_PATTERN = re.compile(r"^[a-zA-Z0-9\s\-\_\.\?]+$")

def validate_query(query: str = Query(..., min_length=1, max_length=250)):
    if not SAFE_QUERY_PATTERN.match(query):
        raise HTTPException(
            status_code=400,
            detail="Query contains unsafe characters. Use only letters, numbers, spaces, and -_.?"
        )
    return query


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
@limiter.limit("5/3minute") 
async def search(request: Request,query: str = Depends(validate_query)):
    """
    Search papers using normalized & tokenized query.
    Returns JSON: { papers: [ {title, authors, year, url, pdfUrl, source, abstract} ] }
    """
    print("=== New search request ===")
    print("Raw query:")
    print(query)
    print("----")

    # 1️⃣ Normalize & tokenize
    try:
        terms = normalize_and_tokenize(query)
    except Exception as e:
        print("Error during NLP processing:", e)
        raise HTTPException(status_code=500, detail="NLP processing failed.")

    print("Normalized terms (tokens):", terms)
    print("----")

    # 2️⃣ Build semantic query string
    semantic_query = " ".join(terms) if terms else query
    print(f"Semantic query being sent to external API: {semantic_query}")

    # 3️⃣ Fetch papers from Semantic Scholar
    try:
        papers = search_semantic_scholar(semantic_query, limit=20)
        
    except Exception as e:
        print("Error fetching from semantic API:", e)
        raise HTTPException(status_code=502, detail="External semantic API failed.Please try again after few seconds")

    # 4️⃣ Log retrieved papers
    print(f"Retrieved {len(papers)} papers. Listing (title - url):")
    for p in papers:
        print("-", p.get("title"), "-", p.get("url") or p.get("pdfUrl"))
    print("=== End search request ===\n")


    papers_top10 = rank_papers(query, papers, top_n=10)

    return {"papers": papers_top10}
     # ✅ frontend expects `papers`




class Paper(BaseModel):
    url: Optional[str] = None
    abstract: Optional[str] = None
    pdfURL:Optional[str]=None
    title: Optional[str] = None

class SummarizeRequest(BaseModel):
    papers: List[Paper]


@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    """
    Accepts a list of papers with `url` and/or `abstract`.
    Summarizes using abstract if available, otherwise fetches content from URL.
    """
    results = {}

    for paper in req.papers:
        key = paper.url or paper.pdfURL or "abstract"
        summary_text = None

        # 1️⃣ Try summarization (keep using existing endpoints)
        try:
            if paper.abstract:
                summary_text = summarize_with_gemini(paper.abstract)
            elif paper.pdfURL:
                summary_text = summarize_url(paper.pdfURL)
            elif paper.url:
                summary_text = summarize_url(paper.url)
           
        except Exception:
            summary_text = None

        # 2️⃣ Determine if summary is valid
        def is_valid_summary(text: str) -> bool:
            if not text or len(text.strip()) < 20:
                return False
            lowered = text.strip().lower()
            invalid_starts = ["error", "unsupported", "no content","please provide the content"]
            return not any(lowered.startswith(start) for start in invalid_starts)

        text_for_classification = ""
        if paper.abstract:
            text_for_classification += paper.abstract + " "
        if paper.title:
            text_for_classification += paper.title
       

        if is_valid_summary(summary_text):
            text_for_classification = summary_text
        else:
            text_for_classification = paper.title or "Unknown"
            summary_text = "Summary not available for this paper at the moment."

        # 3️⃣ Classify topic
        try:
            topic = classify_topic(text_for_classification)
        except Exception as e:
            topic = f"Error classifying topic: {str(e)}"

        # 4️⃣ Store results
        results[key] = {
            "summary": summary_text,
            "topic": topic
        }

    return {"papers": results}



    
class Feedback(BaseModel):
    name: str
    email: str
    message: str

@app.post("/feedback")
async def send_feedback(data: Feedback):
    try:
        # Configure your SMTP (example: Gmail)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "paperforge5@gmail.com"  # PaperForge mail
        password = "wnnn rlsq desr tvdz"

        msg = MIMEText(
            f"Feedback from: {data.name} <{data.email}>\n\n{data.message}"
        )
        msg["Subject"] = "📩 New Feedback from PaperForge"
        msg["From"] = sender_email
        msg["To"] = sender_email  # send to self

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, sender_email, msg.as_string())

        return {"status": "success", "message": "Feedback sent!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}



@app.post("/gap-analysis")
async def gap_analysis(files: List[UploadFile] = File(...)):
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Please upload at least two research papers.")

    file_paths = []
    try:
        # Save uploaded files temporarily
        for file in files:
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as f:
                f.write(await file.read())
            file_paths.append(temp_path)

        # Run the pipeline
        result = run_gap_analysis(file_paths)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gap analysis failed: {str(e)}")

    finally:
        # Cleanup temp files
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)

    # Ensure all keys exist so frontend doesn't crash
    for key in ["common_areas", "unique_contributions", "gaps", "future_research_directions"]:
        if key not in result or result[key] is None:
            result[key] = [] if key != "unique_contributions" else {}

    return result