import { useState, useEffect } from "react";
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
  const [darkMode, setDarkMode] = useState(false);

  // Apply theme to body
  useEffect(() => {
    document.body.setAttribute("data-theme", darkMode ? "dark" : "light");
  }, [darkMode]);

  async function handleSearch(q) {
    setError("");
    setLoading(true);
    setHasSearched(true);
    setQuery(q);
    try {
      const data = await searchPapers(q);
      setResults(Array.isArray(data.papers) ? data.papers : []);
    } catch (e) {
      setError("Something went wrong fetching papers. Using mock data if enabled.");
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <header className="header">
        <div className="brand">
          <img src="/file.png" alt="Paper Forge Logo" className="logo" />
          <div>
            <h1>Paper Forge</h1>
            <div className="tag">Academic Literature Review AI Agent</div>
          </div>
        </div>
        <button 
          className="themeToggle"
          onClick={() => setDarkMode(prev => !prev)}
        >
          {darkMode ? "🌞 Light" : "🌙 Dark"}
        </button>
      </header>

      <main className="main">
        <section className="hero">
          <h2>Meet your Intelligent Research Partner</h2>
          <p>Search a topic or paste a detailed.</p>
          <p>The you would get high quality papers</p>
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
          <div className="resultsMeta">No results. Try another query.</div>
        )}

      </main>
    </>
  );
}
