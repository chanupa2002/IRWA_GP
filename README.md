# 📄 Paper Forge: AI-Driven Research Assistant

Paper Forge is a comprehensive, AI-driven research assistant designed to help students, researchers, and academics streamline the process of finding, analyzing, and summarizing academic papers. It intelligently automates the end-to-end research workflow, offering an all-in-one platform for academic exploration.

---

## ✨ Key Features & Functionality

The system is composed of multiple specialized components, each responsible for a specific stage in the research workflow.

| Component             | Functionality                                                                                   | Core Technology                                         |
|----------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| Paper Finder          | Retrieves relevant, high-quality research papers based on user queries, connecting securely to the Semantic Scholar API. | Semantic Scholar Graph API, HTTPX                      |
| Paper Ranking         | Ranks papers using a hybrid scoring approach that combines textual relevance (TF-IDF/cosine similarity) with academic credibility (citation-based weighting). | TF-IDF, Cosine Similarity                               |
| Summarization Agent   | Converts complex academic content into concise, structured summaries, highlighting the background, methodology, results, and contributions. | Gemini 2.5-Flash (with BART/Local Transformers as fallback) |
| Topic Classification  | Automatically categorizes papers into relevant academic domains and sub-disciplines.          | Gemini 2.5-Flash                                       |
| Gap Analysis Agent    | Performs comparative research analysis across multiple uploaded papers to identify common patterns, unique contributions, and unexplored research gaps. | Gemini-based comparative analysis                       |
| Topic Recommendation  | Provides intelligent suggestions for new or emerging research topics based on the gap analysis and user's field of interest. | Gemini 2.5-Flash                                       |
| Feedback Module       | Processes user feedback (e.g., Complaint, Suggestion) via text classification and automatically forwards it to administrators. | SMTP Email                                             |

---

## 💻 Tech Stack & Design

Paper Forge integrates a modern frontend, a robust backend, and AI-driven services, built with modularity, scalability, and robustness in mind.

| Component       | Technology            | Role                                                  |
|----------------|----------------------|------------------------------------------------------|
| Frontend       | ReactJS              | Responsive and user-friendly interface.             |
| Backend/API    | FastAPI              | Central API layer handling frontend requests.       |
| AI Integration | Gemini 2.5-Flash     | Used for core summarization, classification, and recommendation. |
| Data Retrieval | Semantic Scholar API | Secure connection to fetch relevant academic papers. |

---

## 🛡️ Responsible AI & Security Practices

Security and confidentiality are paramount. The design adheres strictly to ethical AI principles:

- **Ethical Data Handling:** User query information is processed ephemerally (not permanently saved) to protect privacy. All data transmission is conducted over secure, encrypted channels (TLS).  
- **Backend Proxying:** The backend server acts as a proxy, securely forwarding requests to external APIs (e.g., Gemini) using protected credentials. This safeguards sensitive API keys from exposure in the browser.  
- **Transparency:** The system clearly shows the origin and traceability of every research article, displaying the source journal and author. A direct link is provided to the primary source for verification.  
- **Fairness:** Models are selected to minimize bias, and data is integrated from diverse and multidisciplinary sources to ensure balanced recommendations.  

---
## 🤝 Contribution

| IT Number       | Name of the Contributor         |
|-----------------|--------------------------------|
| IT23304024      | A.K.D.C.A. Kanchana            |
| IT23304406      | A.P. Nimsara                   |
| IT23164512      | D.P.I.N. Amararathne           |
| IT23234970      | H.C.S. Rajapaksha              |

---

## 📄 License

This project is licensed under the MIT License. The full text of the license, including copyright information for transparency.

**MIT License**  
Copyright (c)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



## 🛠️ Getting Started (Installation)

To set up the project, you must clone the repository and configure the necessary environment variables for the external APIs.

```bash
git clone https://github.com/chanupa2002/IRWA_GP
cd IRWA_GP

# Navigate to backend directory
pip install -r requirements.txt
# Run the server after configuring environment variables
uvicorn main:app --reload

# Navigate to frontend directory
npm install
npm start
