const BASE_URL = "http://localhost:8000"; // change to your Python backend

async function apiFetch(path, options = {}) {
  const token = localStorage.getItem("auth_token");
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };
  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `HTTP ${res.status}`);
  }
  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}

export const AuthAPI = {
  async login(username, password) {
    // Example (adjust to your backend contract):
    // return apiFetch("/auth/login", { method: "POST", body: JSON.stringify({ username, password }) });
    // For now, mock success:
    if (!username || !password) throw new Error("Missing credentials");
    return { token: "demo-token", user: { username } };
  },
  async me() {
    return { username: "demo-user" };
  },
};

export const NLPAPI = {
  async summarize(query) {
    // return apiFetch("/summarize", { method: "POST", body: JSON.stringify({ query }) });
    // Mock response:
    await new Promise(r => setTimeout(r, 600));
    return { summary: `• Summary for "${query}"\n- Key point A\n- Key point B\n- Key point C` };
  },
  async classify(query) {
    // return apiFetch("/classify", { method: "POST", body: JSON.stringify({ query }) });
    await new Promise(r => setTimeout(r, 600));
    return { topic: "Neural Networks", confidence: 0.92 };
  },
};

export const TokenAPI = {
  async list() {
    // return apiFetch("/tokens", { method: "GET" });
    return [{ id: "tok_1", label: "Default token", createdAt: new Date().toISOString() }];
  },
  async create(label) {
    // return apiFetch("/tokens", { method: "POST", body: JSON.stringify({ label }) });
    return { id: `tok_${Math.random().toString(36).slice(2, 8)}`, label, createdAt: new Date().toISOString() };
  },
  async revoke(id) {
    // return apiFetch(`/tokens/${id}`, { method: "DELETE" });
    return { ok: true };
  },
};
