import { useState } from "react";

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
      files.forEach(file => formData.append("files", file));

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

  return (
    <div className="gap-analysis">
      <h2>Gap Analysis</h2>
      <input type="file" multiple accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleSubmit} disabled={loading}>Analyze Gaps</button>

      {loading && <p style={{ color: "blue" }}>🔄 Analyzing papers, please wait...</p>}
      {error && <p style={{ color: "red" }}>❌ {error}</p>}

      {analysis && (
        <div>
          <h3>Common Areas:</h3>
          <ul>{analysis.common_areas.map((item, i) => <li key={i}>{item}</li>)}</ul>

          <h3>Unique Contributions:</h3>
          {Object.keys(analysis.unique_contributions).map((paper, i) => (
            <div key={i}>
              <h4>{paper}</h4>
              <ul>
                {analysis.unique_contributions[paper].map((point, j) => <li key={j}>{point}</li>)}
              </ul>
            </div>
          ))}

          <h3>Gaps Not Addressed:</h3>
          <ul>{analysis.gaps.map((gap, i) => <li key={i}>{gap}</li>)}</ul>

          <h3>Future Research Directions:</h3>
          <ul>{analysis.future_research_directions.map((dir, i) => <li key={i}>{dir}</li>)}</ul>
        </div>
      )}
    </div>
  );
}
