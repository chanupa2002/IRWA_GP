import React from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";

export default function Topbar() {
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const logout = () => {
    localStorage.removeItem("auth_token");
    navigate("/", { replace: true });
  };

  // hide on login page
  if (pathname === "/") return null;

  return (
    <header className="topbar">
      <div className="topbar-inner">
        <div className="brand">LitReview</div>
        <nav className="nav-links">
          <Link className="nav-link" to="/home">Home</Link>
          <Link className="nav-link" to="/account">Account</Link>
          <Link className="nav-link" to="/tokens">Tokens</Link>
          <button className="btn ghost" onClick={logout}>Logout</button>
        </nav>
      </div>
    </header>
  );
}
