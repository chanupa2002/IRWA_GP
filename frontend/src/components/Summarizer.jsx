import { useState } from "react";
import ResultCard from "./ResultCard";
import "./Summarizer.css"; // new CSS file for custom styles

export default function Summarizer({ results }) {
  const [selectedPaper, setSelectedPaper] = useState(null);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSummarize() {
    if (!selectedPaper) return;

    setLoading(true);
    setError("");
    setSummary("");

    try {
      const response = await fetch("http://localhost:8000/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        
          papers: [
            {
              url: selectedPaper.url,
              pdfURL: selectedPaper.pdfUrl,
              abstract: selectedPaper.abstract,
            },
          ],
        
        }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
     

      const data = await response.json();
      const key = selectedPaper.url || selectedPaper.pdfUrl || "abstract";
      setSummary(data.summaries[key]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="summarizer">
      <h2>Summarization & Classification</h2>

      {results.length === 0 && <p>No papers available for summarization.</p>}

      {results.length > 0 && (
        <>
          <div className="grid">
            {results.map((paper, idx) => (
              <div
                key={paper.id || paper.url || idx}
                className={`summ-card ${selectedPaper === paper ? "selected" : ""}`}
              >
                <label>
                  <input
                    type="radio"
                    name="selectedPaper"
                    checked={selectedPaper === paper}
                    onChange={() => setSelectedPaper(paper)}
                  />
                  <ResultCard doc={paper} />
                </label>
              </div>
            ))}
          </div>

          <button
            className="btn primary summarize-btn"
            onClick={handleSummarize}
            disabled={!selectedPaper || loading}
          >
            {loading ? "Summarizing…" : "Summarize"}
          </button>

          {error && <div className="error">{error}</div>}

          {summary && (
            <div className="summary">
              <h3>Summary:</h3>
              <p>{summary}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
