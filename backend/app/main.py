from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .nlp import normalize_and_tokenize
from .semantic import search_semantic_scholar

app = FastAPI(title="PaperForge Backend")

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
async def search(query: str = Query(..., min_length=1)):
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
        raise HTTPException(status_code=502, detail="External semantic API failed.")

    # 4️⃣ Log retrieved papers
    print(f"Retrieved {len(papers)} papers. Listing (title - url):")
    for p in papers:
        print("-", p.get("title"), "-", p.get("url") or p.get("pdfUrl"))
    print("=== End search request ===\n")

    return {"papers": papers}  # ✅ frontend expects `papers`
