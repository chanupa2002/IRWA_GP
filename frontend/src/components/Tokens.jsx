import React, { useEffect, useState } from "react";
import { TokenAPI } from "../api";

export default function Tokens() {
  const [tokens, setTokens] = useState([]);
  const [label, setLabel] = useState("");
  const [busy, setBusy] = useState(false);

  const refresh = async () => {
    const list = await TokenAPI.list();
    setTokens(list);
  };

  useEffect(() => {
    refresh();
  }, []);

  const create = async () => {
    if (!label.trim()) return;
    setBusy(true);
    try {
      const t = await TokenAPI.create(label.trim());
      setLabel("");
      setTokens((prev) => [t, ...prev]);
    } finally {
      setBusy(false);
    }
  };

  const revoke = async (id) => {
    setBusy(true);
    try {
      await TokenAPI.revoke(id);
      setTokens((prev) => prev.filter((t) => t.id !== id));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="container">
      <div className="stack">
        <div className="card">
          <h2 className="section-title">Token Management</h2>
          <div className="subtle">Create and revoke API tokens.</div>

          <div className="row" style={{ marginTop: 14 }}>
            <input
              className="input"
              value={label}
              onChange={(e) => setLabel(e.target.value)}
              placeholder="Token label (e.g., 'Backend Service')"
            />
            <button className="btn" onClick={create} disabled={busy}>
              {busy ? "Working..." : "Create Token"}
            </button>
          </div>
        </div>

        <div className="card">
          <h3 className="section-title">Your Tokens</h3>
          {tokens.length === 0 ? (
            <div className="subtle">No tokens yet.</div>
          ) : (
            <div className="stack" style={{ marginTop: 8 }}>
              {tokens.map((t) => (
                <div key={t.id} className="row" style={{ justifyContent: "space-between" }}>
                  <div>
                    <div><b>{t.label || t.id}</b></div>
                    <div className="subtle">{t.id} · {new Date(t.createdAt).toLocaleString()}</div>
                  </div>
                  <button className="btn danger" onClick={() => revoke(t.id)} disabled={busy}>
                    Revoke
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
