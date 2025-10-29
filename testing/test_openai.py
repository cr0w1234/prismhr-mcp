from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(override=True)
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

CLOUD_RUN_URL = os.getenv('MCP_SERVER_URL', 'http://localhost:8080/mcp/') # "https://test-mcp-server-82241824210.us-central1.run.app/mcp/" # "http://localhost:8080", "https://mcp-server-xtjhu227ga-uc.a.run.app", "https://mcp-server-82241824210.us-central1.run.app"

# test_mcp_server
resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "prismhr-mcp-server",
            "server_url": CLOUD_RUN_URL,
            "require_approval": "never",
        },
    ],
    input="if my client id is 132 give me information about my employees. also, what are the possible pto codes?",


)

print(resp.output_text)