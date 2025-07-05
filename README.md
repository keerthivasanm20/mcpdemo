# 🧠 Internal Research Agent for KeerthiMNC

An intelligent, LangChain-powered AI agent built to handle complex internal employee queries at KeerthiMNC. This system uses a modular architecture of tools to deliver contextual, accurate, and actionable responses by integrating HR documents, insurance policies, and live industry data.

---

## 🚀 Demo

🎥 [Watch the Demo Video](#) *(https://github.com/keerthivasanm20/mcpdemo/tree/main/presidio_agent/demo-video)*

---

## 🧩 Tools & Capabilities

### 🔍 1. RAG Tool (HR Policy Assistant)
- Uses `ChromaDB` and `HuggingFace` embeddings to vectorize HR policy documents (`knowledge.txt`).
- Answers queries like:
  - “What is the policy on remote work?”
  - “Is there a leave carry-forward provision?”

### 📄 2. MCP Tool (Insurance Policy Assistant)
- Connects to a live **MCP server** using Amazon Bedrock's Claude model.
- Integrates with **Google Docs API** to extract real-time insurance-related information.
- Sample queries:
  - “What are my health coverage limits?”
  - “How do I file a reimbursement?”

### 🌐 3. Web Search Tool (Trends & Compliance Insights)
- Uses Anthropic Claude 3 on Bedrock to simulate industry benchmarking, regulatory updates, and AI policy analysis.
- Answers include:
  - “Compare our hiring rate with industry benchmarks.”
  - “Summarize compliance policies on AI data handling.”

---

## 🧠 Sample Use Cases

- ✅ “Summarize all customer feedback related to our Q1 marketing campaigns.”
- ✅ “Find relevant compliance policies related to AI data handling.”
- ✅ “Compare our current hiring trend with industry benchmarks.”
- ✅ “What are the consequences of missing office attendance?”

---

## 🏗️ Tech Stack

| Component        | Technology                              |
|------------------|------------------------------------------|
| Framework        | LangChain + Django + FastAPI             |
| LLM Backend      | Amazon Bedrock + Anthropic Claude 3      |
| Embedding Model  | HuggingFace `all-MiniLM-L6-v2`           |
| Vector DB        | ChromaDB (local persistent)              |
| Document Loader  | `knowledge.txt` via LangChain TextLoader |
| Google Docs API  | For real-time insurance policy answers   |

