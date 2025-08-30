import { useState } from "react";
import { FiSearch } from "react-icons/fi";

export default function SearchBar({ onSearch, loading }) {
  const [value, setValue] = useState("");

  const submit = (e) => {
    e.preventDefault();
    const q = value.trim();
    if (!q) return;
    onSearch(q);
  };

  return (
    <form className="searchWrap" onSubmit={submit} role="search" aria-label="Paper search">
      <div className="searchCard">
        <div style={{display:"flex", alignItems:"center", gap:12, padding:"8px 12px"}}>
          <FiSearch size={22} style={{opacity:.7}} />
          <input
            value={value}
            onChange={(e)=>setValue(e.target.value)}
            placeholder="Search topics, questions, or paste a long query…"
            aria-label="Search query"
            style={{
              flex:1, border:"none", outline:"none", fontSize:18, padding:"10px 4px",
              background:"transparent"
            }}
          />
          <button className="btn primary" type="submit" disabled={loading} aria-busy={loading}>
            {loading ? "Searching…" : "Search"}
          </button>
        </div>
      </div>
    </form>
  );
}
