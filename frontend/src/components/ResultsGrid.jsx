import ResultCard from "./ResultCard";

export default function ResultsGrid({ results }) {
  return (
    <div className="grid">
      {results.map(r => <ResultCard key={r.id || r.url} doc={r} />)}
    </div>
  );
}
