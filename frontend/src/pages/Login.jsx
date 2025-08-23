import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthAPI } from "../api";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      const res = await AuthAPI.login(username, password);
      localStorage.setItem("auth_token", res.token);
      navigate("/home", { replace: true });
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="center">
      <form className="card" onSubmit={onSubmit} style={{ width: 380 }}>
        <h2 className="section-title">Sign in</h2>
        <div className="subtle">Welcome to LitReview — please sign in.</div>
        <div className="form" style={{ marginTop: 16 }}>
          <label className="label">Username</label>
          <input
            className="input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="you@example.com"
            autoFocus
          />
          <label className="label">Password</label>
          <input
            className="input"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
          />
          {error && (
            <div className="subtle" style={{ color: "#ff8b8b" }}>{error}</div>
          )}
          <button className="btn" disabled={busy} type="submit">
            {busy ? "Signing in..." : "Sign in"}
          </button>
        </div>
      </form>
    </div>
  );
}
