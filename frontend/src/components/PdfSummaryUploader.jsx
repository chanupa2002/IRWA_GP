import { useState } from "react";
import "./PdfSummaryUploader.css";

export default function PdfSummaryUploader() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [topic, setTopic] = useState("");
  const [topicLoading, setTopicLoading] = useState(false);

  const handleTopicClassifier = async () => {
    if (!summary) return;
    setTopicLoading(true);
    try {
      const res = await fetch("http://localhost:8000/topicClassifier-pdf/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ summary }),
      });
      const data = await res.json();
      setTopic(data.topic);
    } catch (error) {
      setTopic("Error in topic classification");
    } finally {
      setTopicLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setSummary("");
    setFilename("");

    try {
      const res = await fetch("http://localhost:8000/summarize-pdf/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setFilename(data.filename || file.name);
      setSummary(data.summary);
    } catch (err) {
      console.error(err);
      setFilename(file.name);
      setSummary("Error uploading or summarizing PDF.");
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFile(null);
    setFilename("");
    setSummary("");
    setTopic("");
  };

  return (
    <div className="pdf-uploader">
      <h2>📄 PDF Summary & Topic Classifier</h2>

      <div className="upload-section">
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button onClick={handleUpload} disabled={loading || !file}>
          {loading ? "Summarizing..." : "Upload & Summarize"}
        </button>
        <button onClick={handleClear} className="clear-btn">
          Clear
        </button>
      </div>

      {filename && (
        <div className="file-info">
          <strong>File:</strong> {filename}
        </div>
      )}

      {summary && (
        <div className="summary-box">
          <h3>Summary:</h3>
          <p>{summary}</p>

          <button
            onClick={handleTopicClassifier}
            disabled={topicLoading}
            className="classify-btn"
          >
            {topicLoading ? "Classifying..." : "Classify Topic"}
          </button>

          {topic && (
            <div className="topic-box">
              <h4>Identified Topic:</h4>
              <p>{topic}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
