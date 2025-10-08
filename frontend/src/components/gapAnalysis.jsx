import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./GapAnalysis.css";

export default function GapAnalysis() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
    setAnalysis(null);
    setError("");
  };

  const handleSubmit = async () => {
    if (files.length < 2) {
      setError("Please upload at least two research papers.");
      return;
    }

    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const formData = new FormData();
      files.forEach((file) => formData.append("files", file));

      const response = await fetch("http://localhost:8000/gap-analysis", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error(`Status: ${response.status}`);
      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFiles([]);
    setAnalysis(null);
    setError("");
  };

  return (
    <div className="gap-analysis">
      <h2>🧩 Research Gap Analysis</h2>

      <div className="upload-area">
        <input
          type="file"
          multiple
          accept="application/pdf"
          onChange={handleFileChange}
        />
        <div className="buttons">
          <button onClick={handleSubmit} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Gaps"}
          </button>
          <button onClick={handleClear} className="clear-btn">
            Clear
          </button>
        </div>
      </div>

      {loading && <p className="loading">🔄 Analyzing papers, please wait...</p>}
      {error && <p className="error">❌ {error}</p>}

      {analysis && (
        <div className="analysis-results">
          <section>
            <h3>🔹 Common Areas</h3>
            <ReactMarkdown>{analysis.common_areas.join("\n")}</ReactMarkdown>
          </section>

          <section>
            <h3>🧠 Unique Contributions</h3>
            {Object.keys(analysis.unique_contributions).map((paper, i) => (
              <div key={i} className="paper-section">
                <h4>{paper}</h4>
                <ReactMarkdown>
                  {analysis.unique_contributions[paper].join("\n")}
                </ReactMarkdown>
              </div>
            ))}
          </section>

          <section>
            <h3>🚧 Gaps Not Addressed</h3>
            <ReactMarkdown>{analysis.gaps.join("\n")}</ReactMarkdown>
          </section>

          <section>
            <h3>🚀 Future Research Directions</h3>
            <ReactMarkdown>
              {analysis.future_research_directions.join("\n")}
            </ReactMarkdown>
          </section>
        </div>
      )}
    </div>
  );
}
