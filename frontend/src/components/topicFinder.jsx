import { useState } from "react";
import "./TopicFinder.css";

export default function TopicFinder() {
  const [paragraph, setParagraph] = useState("");
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!paragraph.trim()) {
      setError("Please enter a paragraph to generate topics.");
      return;
    }

    setLoading(true);
    setError("");
    setTopics([]);

    try {
      const response = await fetch("http://localhost:8000/generate-topics", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ paragraph }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || `Status: ${response.status}`);
      }

      const data = await response.json();
      setTopics(data.topics || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyTopic = (topic) => {
    navigator.clipboard.writeText(topic);
    alert(`Copied: ${topic}`);
  };

  const handleCopyAll = () => {
    navigator.clipboard.writeText(topics.join("\n"));
    alert("All topics copied!");
  };

  const handleClear = () => {
    setParagraph("");
    setTopics([]);
    setError("");
  };

  return (
    <div className="topic-finder">
      <h2>Research Topic Finder</h2>
      <textarea
        rows={6}
        placeholder="Paste your research paragraph here..."
        value={paragraph}
        onChange={(e) => setParagraph(e.target.value)}
      />
      <div className="char-count">
        Character count: {paragraph.length}
      </div>
      <div className="buttons">
        <button onClick={handleSubmit} disabled={loading}>
          {loading ? <span className="spinner">⏳ Generating...</span> : "Generate Topics"}
        </button>
        <button onClick={handleClear}>Clear</button>
      </div>

      {error && <p className="error">❌ {error}</p>}

      {topics.length > 0 && (
        <div className="results">
          <h3>Suggested Research Topics:</h3>
          <button className="copy-all" onClick={handleCopyAll}>
            📋 Copy All Topics
          </button>
          <ul>
            {topics.map((topic, i) => (
              <li key={i} className="topic-item">
                {topic}{" "}
                {/* <button
                  className="copy-btn"
                  onClick={() => handleCopyTopic(topic)}
                >
                  
                </button> */}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
