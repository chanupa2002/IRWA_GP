import React, { useState } from "react";
import { NLPAPI } from "../api";

export default function Home() {
  const [query, setQuery] = useState("");
  const [sumResult, setSumResult] = useState("");
  const [clsResult, setClsResult] = useState("");
  const [busy, setBusy] = useState({ sum: false, cls: false });

  const doSummarize = async () => {
    if (!query.trim()) return;
    setBusy((b) => ({ ...b, sum: true }));
    setSumResult("");
    try {
      const res = await NLPAPI.summarize(query.trim());
      setSumResult(res.summary || String(res));
    } catch (e) {
      setSumResult(`Error: ${e.message}`);
    } finally {
      setBusy((b) => ({ ...b, sum: false }));
    }
  };

  const doClassify = async () => {
    if (!query.trim()) return;
    setBusy((b) => ({ ...b, cls: true }));
    setClsResult("");
    try {
      const res = await NLPAPI.classify(query.trim());
      setClsResult(`Topic: ${res.topic}\nConfidence: ${(res.confidence * 100).toFixed(1)}%`);
    } catch (e) {
      setClsResult(`Error: ${e.message}`);
    } finally {
      setBusy((b) => ({ ...b, cls: false }));
    }
  };

  return (
    <div className="container">
      <div className="stack">
        <div className="card">
          <h2 className="section-title">Literature Review Tools</h2>
          <div className="subtle">Enter a keyword or query to analyze.</div>

          <div className="stack" style={{ marginTop: 14 }}>
            <input
              className="input"
              placeholder="e.g., transfer learning for medical imaging"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />

            <div className="row">
              <button className="btn" onClick={doSummarize} disabled={busy.sum}>
                {busy.sum ? "Summarizing..." : "Summarize"}
              </button>
              <button className="btn" onClick={doClassify} disabled={busy.cls}>
                {busy.cls ? "Classifying..." : "Topic Classify"}
              </button>
            </div>
          </div>

          <div className="results">
            {sumResult && (
              <div className="card">
                <div className="label">Summary</div>
                <div className="result-block">{sumResult}</div>
              </div>
            )}
            {clsResult && (
              <div className="card">
                <div className="label">Classification</div>
                <div className="result-block">{clsResult}</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
