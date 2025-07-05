# agentapp/langchain_backend/agent.py
import boto3
from langchain.agents import initialize_agent, Tool
from langchain_aws import ChatBedrock
from .tools import get_claude_search_tool, get_rag_tool, mcp_tool
import vars

def build_agent():
    session = boto3.Session(
        aws_access_key_id=vars.AWS_ACCESS_KEY,
        aws_secret_access_key=vars.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )

    bedrock = session.client('bedrock-runtime')
    llm = ChatBedrock(
        client=bedrock,
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # or your preferred model
        model_kwargs={
            "max_tokens": 512,
        }
    )
    tools = [
        Tool(name="RAG Tool", func=get_rag_tool(llm), description="HR policy questions."),
        Tool(name="MCP Tool", func=mcp_tool, description="Insurance questions."),
        Tool(name="Web Search Tool", func=get_claude_search_tool(llm), description="Simulated web search for benchmarks & trends.")
    ]

    agent = initialize_agent(
        tools,
        llm,
        agent_type="zero-shot-react-description",
        verbose=True
    )
    return agent
