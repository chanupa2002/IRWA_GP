import { HiOutlineDocumentText } from "react-icons/hi";

export default function ResultCard({ doc }) {
  const authors = Array.isArray(doc.authors) ? doc.authors.join(", ") : doc.authors;
  return (
    <article className="card">
      <div className="cardHead">
        <div className="fileIcon"><HiOutlineDocumentText size={22} /></div>
        <div>
          <h3 className="title">
            <a href={doc.url} target="_blank" rel="noreferrer">{doc.title}</a>
          </h3>
          <div className="meta">
            {authors ? `${authors} · ` : ""}{doc.venue}{doc.year ? ` · ${doc.year}` : ""}{doc.source ? ` · ${doc.source}` : ""}
          </div>
        </div>
      </div>

      {doc.abstract && <p className="abstract">{doc.abstract}</p>}

      <div className="actions">
        <a className="btn primary" href={doc.url} target="_blank" rel="noreferrer">Open Paper</a>
        {doc.pdfUrl && <a className="btn" href={doc.pdfUrl} target="_blank" rel="noreferrer">PDF</a>}
      </div>
    </article>
  );
}
