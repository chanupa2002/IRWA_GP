import axios from "axios";
import { mockResults } from "./mockResults";

/**
 * searchPapers:
 * - If REACT_APP_USE_MOCK=true or no backend URL, returns mock results (simulated delay).
 * - Else GETs /search?query=... from your backend.
 *   Expected backend response shape:
 *   { papers: [{ id, title, authors[], year, venue, url, pdfUrl, source, abstract }] }
 */
export async function searchPapers(query){
  const useMock = String(process.env.REACT_APP_USE_MOCK || "").toLowerCase() === "true";
  const base = process.env.REACT_APP_API_BASE_URL;

  if (useMock || !base) {
    await new Promise(r => setTimeout(r, 600)); // small UX delay
    return { papers: mockResults };
  }

  // Call backend endpoint
  const res = await axios.get(`${base}/search`, {
    params: { query }
  });
  return res.data; // should contain { papers: [...] }
}
