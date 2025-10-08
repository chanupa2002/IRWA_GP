import { useState } from "react";
import "./index.css";
import "./App.css";
import SearchBar from "./components/SearchBar";
import ResultsGrid from "./components/ResultsGrid";
import Summarizer from "./components/Summarizer"; // Import new component
import { searchPapers } from "./api";
import FeedbackForm from "./components/FeedbackForm";
import GapAnalysis from "./components/gapAnalysis";
import TopicFinder from "./components/topicFinder";
import PdfSummaryUploader from "./components/PdfSummaryUploader";
import StickyFeedback from "./components/StickyFeedback";
import Footer from "./components/Footer";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  const [activeTab, setActiveTab] = useState("search");

  async function handleSearch(q) {
    setError("");
    setLoading(true);
    setHasSearched(true);
    setQuery(q);
    try {
      const data = await searchPapers(q);
      setResults(Array.isArray(data.papers) ? data.papers : []);
      if (!data.papers || data.papers.length === 0) {
        setError("No results found. Try a broader query.");
      }
    } catch (e) {
      var backendMessage =
        e.response?.data?.detail || e.message || "Unexpected error occurred.";
      if (e.response?.status === 502) {
        backendMessage =
          "The research service is busy. Please wait a few seconds and try again.";
      }

      setError(backendMessage);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <header className="header">
        <div className="brand">
          <div className="logo" />
          <div>
            <h1>Paper Forge</h1>
            <div className="tag">Academic Literature Review AI Agent</div>
          </div>
        </div>
      </header>

      <main className="main">
        <div className="tabs">
          <button
            className={activeTab === "search" ? "tab active" : "tab"}
            onClick={() => setActiveTab("search")}
          >
            Search
          </button>
          <button
            className={activeTab === "summarizer" ? "tab active" : "tab"}
            onClick={() => setActiveTab("summarizer")}
            disabled={!hasSearched}
          >
            Summarization & Classification
          </button>
          <button
            className={activeTab === "gapAnalysis" ? "tab active" : "tab"}
            onClick={() => setActiveTab("gapAnalysis")}
          >
            Gap Analysis
          </button>
          <button
            className={activeTab === "topicFinder" ? "tab active" : "tab"}
            onClick={() => setActiveTab("topicFinder")}
          >
            Topic Recommendation
          </button>
          <button
            className={activeTab === "uploaderSummary" ? "tab active" : "tab"}
            onClick={() => setActiveTab("uploaderSummary")}
          >
            Uploader Summary
          </button>
        </div>

        {activeTab === "search" && (
          <>
            <section className="hero">
              <h2>Meet your Intelligent Research Partner</h2>
              <p>
                Search a topic or paste a detailed question to find high-quality
                papers.
              </p>
            </section>

            <SearchBar onSearch={handleSearch} loading={loading} />

            {error && <div className="error">{error}</div>}
            {loading && <span className="loading">Finding papers…</span>}

            {!loading && results.length > 0 && (
              <>
                <div className="resultsMeta">
                  Showing {results.length} results for “{query}”
                </div>
                <ResultsGrid results={results} />
              </>
            )}

            {!loading && hasSearched && results.length === 0 && !error && (
              <div className="resultsMeta">
                No results. Try a broader query.
              </div>
            )}
            <div className="footerNote">
              Tip: you can paste a long research prompt or multiple keywords.
            </div>
          </>
        )}

        {activeTab === "summarizer" && <Summarizer results={results} />}

        {activeTab === "gapAnalysis" && <GapAnalysis />}
        {activeTab == "topicFinder" && <TopicFinder />}
        {activeTab == "uploaderSummary" && <PdfSummaryUploader />}
      </main>

      <StickyFeedback />

      <Footer />
    </>
  );
}
