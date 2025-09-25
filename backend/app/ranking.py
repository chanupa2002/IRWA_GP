from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_papers(query: str, papers: List[Dict], top_n: int = 10) -> List[Dict]:
    """
    Rank papers by a combination of:
    1. Cosine similarity between query and paper title+abstract
    2. Number of citations (if available, fallback to 0)
    Returns top_n papers.
    """
    if not papers:
        return []

    # 1️⃣ Build text corpus: title + abstract
    corpus = []
    for paper in papers:
        text = (paper.get("title") or "") + " " + (paper.get("abstract") or "")
        corpus.append(text)

    # 2️⃣ TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([query] + corpus)
    
    # 3️⃣ Cosine similarity with the query (first row)
    query_vec = tfidf_matrix[0]
    paper_vecs = tfidf_matrix[1:]
    cos_sims = cosine_similarity(query_vec, paper_vecs)[0]  # array of similarities

    # 4️⃣ Handle citations safely
    citations = [p.get("citationCount", 0) or 0 for p in papers]
    max_cite = max(citations) if citations else 1

    # Avoid division by zero
    if max_cite == 0:
        citations_norm = [0 for _ in citations]
    else:
        citations_norm = [c / max_cite for c in citations]

    # 5️⃣ Compute final score (weight: cosine 0.7, citations 0.3)
    final_scores = [0.7 * cos + 0.3 * cite for cos, cite in zip(cos_sims, citations_norm)]

    # 6️⃣ Sort papers by score
    ranked = sorted(zip(papers, final_scores), key=lambda x: x[1], reverse=True)

    # 7️⃣ Return only top_n papers
    top_papers = [p[0] for p in ranked[:top_n]]
    return top_papers
