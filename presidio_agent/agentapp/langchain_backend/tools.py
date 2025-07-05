# agentapp/langchain_backend/tools.py
import requests
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.tools import tool
from .loader import setup_chroma
from langchain.chains import LLMChain
from .loader import setup_chroma  # this uses HuggingFace now

def get_rag_tool(llm):
    """
    Creates a LangChain RetrievalQA tool that answers only Keerthi MNC HR policy questions
    using HuggingFace-embedded internal text documents stored in ChromaDB.
    """
    retriever = setup_chroma()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )

    @tool
    def rag_tool(query: str) -> str:
        """Answer only Keerthi MNC HR policy questions using internal HR documents indexed with HuggingFace embeddings."""
        return qa_chain.run(query)

    return rag_tool

@tool
def mcp_tool(query: str) -> str:
    """Call the MCP API for  only Keerthi MNC insurance-related queries."""
    try:
        res = requests.get(
            "http://localhost:8000/insurance_query",
            params={"prompt": query},
            timeout=60  # 1 minute timeout
        )
        if res.status_code != 200:
            return f"[MCP Tool Error] Received status code {res.status_code} from MCP API"
        return res.json().get("result", "No response from MCP")
    except Exception as e:
        return f"[MCP Tool Error] {e}"


def get_claude_search_tool(llm):
    prompt = PromptTemplate(
        input_variables=["query"],
        template="""
    You are a research assistant for internal corporate strategy.
    Provide a detailed, up-to-date, and summarized answer to this query, assuming you have access to reliable external information sources.

    Query: {query}

    Answer as if you're citing current trends, regulatory updates, or benchmarks (be specific and confident).
    """
        )
    chain = LLMChain(llm=llm, prompt=prompt)

    @tool
    def claude_search_tool(query: str) -> str:
        """Simulate a web search using Claude to return up-to-date and benchmarked insights."""
        return chain.run(query)

    return claude_search_tool
