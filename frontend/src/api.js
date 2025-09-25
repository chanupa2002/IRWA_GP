import axios from "axios";
import { mockResults } from "./mockResults";

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
  return res.data.RES; // should contain { papers: [...] }
}

