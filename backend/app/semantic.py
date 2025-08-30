# semantic.py
import os
import httpx
from typing import List, Dict

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_semantic_scholar(query: str, limit: int = 20) -> List[Dict]:
    """
    Query Semantic Scholar Graph API and return list of paper dicts.
    Optional: set env var SEMANTIC_SCHOLAR_API_KEY for x-api-key header.
    """
    params = {
        "query": query,
        "limit": limit,
        # choose fields we will map
        "fields": "title,authors,year,venue,url,abstract,openAccessPdf"
    }
    headers = {}
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    if key:
        headers["x-api-key"] = key

    with httpx.Client(timeout=20.0) as client:
        r = client.get(SEMANTIC_SCHOLAR_URL, params=params, headers=headers)
        r.raise_for_status()
        data = r.json()
        # data expected to have 'data' list (per API)
        results = []
        for item in data.get("data", []):
            # map authors to list of names
            authors = [a.get("name") for a in item.get("authors", []) if a.get("name")]
            pdfUrl = None
            if item.get("openAccessPdf") and item["openAccessPdf"].get("url"):
                pdfUrl = item["openAccessPdf"]["url"]
            # compose source
            source = "SemanticScholar"
            results.append({
                "id": item.get("paperId") or item.get("paper_id") or item.get("id"),
                "title": item.get("title"),
                "authors": authors,
                "year": item.get("year"),
                "venue": item.get("venue"),
                "url": item.get("url"),
                "pdfUrl": pdfUrl,
                "source": source,
                "abstract": item.get("abstract") or ""
            })
    return results
