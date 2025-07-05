import contextlib
from mcp.server.fastmcp import FastMCP
from google.oauth2 import service_account
from googleapiclient.discovery import build
import boto3
import os
import json
import vars
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
# Create a combined lifespan to manage both session managers

# === Setup Google Docs API ===
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
DOCUMENT_ID = vars.DOCUMENT_ID  # Replace with the actual doc ID

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
docs_service = build('docs', 'v1', credentials=credentials)

AWS_ACCESS_KEY_ID = vars.AWS_ACCESS_KEY  # Replace with your AWS access key
AWS_SECRET_ACCESS_KEY = vars.AWS_SECRET_ACCESS_KEY  # Replace with your AWS secret key
AWS_REGION = 'us-east-1'  # Update region as needed

# === Setup Bedrock (Claude) ===
bedrock = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def fetch_doc_text(doc_id: str) -> str:
    """Fetch and return plain text from a Google Doc."""
    doc = docs_service.documents().get(documentId=doc_id).execute()
    content = doc.get('body', {}).get('content', [])
    text = ""
    for element in content:
        if 'paragraph' in element:
            elements = element['paragraph'].get('elements', [])
            for elem in elements:
                text += elem.get('textRun', {}).get('content', '')
    return text

def ask_claude_bedrock(question: str, context: str) -> str:
    """Send a question and context to Claude via Amazon Bedrock."""

    prompt = (
        "Human: You are an expert insurance policy analyst. "
        "Based on the following document content, answer the user's question.\n\n"
        f"Document:\n{context}\n\n"
        f"Question:\n{question}\n\n"
        "Assistant:"
    )

    session = boto3.Session(
        aws_access_key_id=vars.AWS_ACCESS_KEY,
        aws_secret_access_key=vars.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )

    bedrock = session.client('bedrock-runtime')

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 512,
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body),
        contentType="application/json"
    )

    response_body = response['body'].read()
    body = json.loads(response_body)
    # Adjust based on how Claude's response is structured
    print("Claude Response:", body)  # Debugging line to see the response structure
    if "content" not in body:
        return "No response content found"
    else:
        content = body["content"][0]
        if 'text' in content:
            return content["text"]


# === Initialize MCP Server ===
mcp = FastMCP("Insurance QA MC", stateless_http=True, json_response=True)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield

app = FastAPI(lifespan=lifespan)
app.mount("/demo", mcp.streamable_http_app())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@mcp.tool()
def insurance_query(question: str):
    """Main endpoint to answer insurance questions using Google Docs + Bedrock."""
    context = fetch_doc_text(DOCUMENT_ID)
    return ask_claude_bedrock(question, context)
    # return (question, context)

@app.get("/insurance_query")
async def test_mcp_tool(prompt: str = Query(..., description="User prompt")):
    """Test endpoint to call your MCP tool directly"""
    # This bypasses MCP protocol and calls your tool function directly
    result = insurance_query(prompt)
    return {"result": result}
