import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Topbar from "./components/Topbar";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Home from "./components/Home";
import Account from "./components/Account";
import Tokens from "./components/Tokens";

export default function App() {
  return (
    <div className="app-shell">
      <BrowserRouter>
        <Topbar />
        <Routes>
          <Route path="/" element={<Login />} />
          <Route
            path="/home"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />
          <Route
            path="/account"
            element={
              <ProtectedRoute>
                <Account />
              </ProtectedRoute>
            }
          />
          <Route
            path="/tokens"
            element={
              <ProtectedRoute>
                <Tokens />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/home" replace />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}
