<h1 align="center">🧠 Enterprise Intelligent Search System </h1>

<p align="center">
 <b>Context-Aware Search → Reasoning Agents → Grounded Answers</b>  
</p>
<p align="center">
Built using <b>FastAPI · Streamlit · LangChain · Llama 3 · ChromaDB</b>
</p>

---

## 📚 Table of Contents
- [🔎 Overview](#-overview)
- [💡 Why This Matters](#-why-this-matters)
- [🤖 System Architecture](#-system-architecture)
- [🛠️ Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 How to Run](#-how-to-run)
- [💬 Example Queries](#-example-queries)
- [📎 Answer Format](#-answer-format)
- [🔮 Future Enhancements](#-future-enhancements)
- [👨‍💻 Maintainer](#-maintainer)

---

## 🔎 Overview
This system acts as an **internal "ChatGPT" for the enterprise**, going beyond simple semantic matching to provide **grounded, context-aware answers**. It uses an **LLM-driven agentic workflow** that:

✔ Understands user intent (beyond keywords)  
✔ Decides which sources to query  
✔ Retrieves and ranks relevant evidence  
✔ Synthesizes a **grounded answer**  
✔ Attaches **accurate citations** to every response

> Designed for **low latency**, running fully on a developer machine with enterprise-grade reasoning capabilities.

---

## 💡 Why This Matters

Traditional Enterprise Search & Basic RAG often fail because:

-  Relies only on keyword/semantic similarity
-  Prone to hallucinations (making things up)
-  Lacks explainability

📌 **With this Agentic System**, users get:

> _"A system that thinks before it searches."_

- **Intent Understanding:** Knows what you are asking.
- **Grounded Facts:** Every sentence is backed by retrieved chunks.
- **Trust:** Visible citations and confidence scores.

> 👉 **No more hallucinations. Just facts.**

---

## 🤖 System Architecture

| Component | Responsibility |
|-----------|----------------|
| 🧠 **Query Analysis Agent** | Deconstructs user prompt to understand intent |
| 🔍 **Vector Retrieval** | Queries ChromaDB using Sentence-Transformers |
| 🥇 **Evidence Selection** | Ranks and filters retrieved documents for relevance |
| 📝 **Answer Synthesis** | Generates the final natural language response |
| 📎 **Citation Generator** | Maps specific document excerpts to the answer |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend API | FastAPI |
| Frontend UI | Streamlit |
| Agent Framework | LangChain |
| LLM | Groq (llama-3.1-8b-instant) |
| Vector Database | Chroma |
| Embeddings | Sentence-Transformers |
| Language | Python |

---

## 📁 Project Structure

```bash
enterprise-search-system/
│
├── src/
│   ├── api/                   # FastAPI routes & models
│   ├── agents/                # Agentic orchestration logic
│   ├── storage/               # Vector store (Chroma)
│   ├── connectors/            # Data connectors (Extensible)
│   └── ui/                    # Streamlit UI
│
├── scripts/
│   ├── generate_dummy_data.py # Create sample documents
│   ├── ingest_data.py         # Vectorize & store data
│   └── test.py
│
├── data/
│   ├── documents/             # Raw enterprise docs
│   └── chroma/                # Persisted Vector DB
│
├── .env.example
└── requirements.txt
```
---
###

## 🚀 How to Run

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/SatyamBaghel01/enterprise-search-system
cd enterprise-search-system
```
### 2️⃣ Create a virtual environment  
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```
### 3️⃣ Install dependencies  
```bash
pip install -r backend/requirements.txt
```

### 4️⃣ Configure Environment
Create a .env file and add your Groq API key:
```
GROQ_API_KEY=your_key_here
```

### 5️⃣ Prepare Data (MVP) 
Generate sample data and ingest it into the Vector DB:
```bash
python -m scripts.generate_dummy_data
python -m scripts.ingest_data
```

### 6️⃣ Run the Application
Terminal 1: Backend
```bash
streamlit run frontend/app.py
```
Terminal 2: Frontend
```bash
streamlit run streamlit_app.py
```
### 💬 Example Queries
```bash
“What is enterprise search and how does it work?”
“Explain the system architecture described in the documents”
“Summarize security policies”
“What deployment approaches are mentioned?”
“Which APIs are documented?”
```
---

### 📎 Answer Format
- Natural Language Answer: The synthesized response.
- Confidence Score: How certain the model is.
- Latency: Execution time tracking.
- Retrieved Documents: The raw chunks used.
- Source Citations: Exact excerpts mapping to the answer.

---

### 🔮 Future Enhancements
-  Integration with internal SQL databases
-  Advanced re-ranking algorithms for higher precision
-  User feedback loop (RLHF) for continuous improvement

---

### 👨‍💻 Maintained By
**Satyam Singh Baghel**  
Gen AI Engineer | LLM + Autonomous Agents

---
