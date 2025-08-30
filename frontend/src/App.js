import { useState } from "react";
import "./index.css";
import "./App.css";
import SearchBar from "./components/SearchBar";
import ResultsGrid from "./components/ResultsGrid";
import { searchPapers } from "./api";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [hasSearched, setHasSearched] = useState(false);

  async function handleSearch(q){
    setError("");
    setLoading(true);
    setHasSearched(true);
    setQuery(q);
    try{
      const data = await searchPapers(q);
      setResults(Array.isArray(data.papers) ? data.papers : []); // ✅ FIXED: use data.papers
    }catch(e){
      setError("Something went wrong fetching papers. Using mock data if enabled.");
      setResults([]);
    }finally{
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
        <section className="hero">
          <h2>Meet your intelligent research partner</h2>
          <p>Search a topic or paste a detailed question to find high-quality papers.</p>
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
          <div className="resultsMeta">No results. Try a broader query.</div>
        )}

        <div className="footerNote">Tip: you can paste a long research prompt or multiple keywords.</div>
      </main>
    </>
  );
}
