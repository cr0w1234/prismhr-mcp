from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

load_dotenv(override=True)
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

CLOUD_RUN_URL = os.getenv('MCP_SERVER_URL', 'http://localhost:8080/mcp/')

# Set up dual output: terminal + file
results_file = Path('test_emails_results.txt')
log_file = open(results_file, 'a', encoding='utf-8')

def log_print(*args, **kwargs):
    """Print to both terminal and log file"""
    # Print to terminal
    print(*args, **kwargs)
    # Write to file
    message = ' '.join(str(arg) for arg in args)
    if kwargs.get('end', '\n') != '\n':
        log_file.write(message + kwargs.get('end', '\n'))
    else:
        log_file.write(message + '\n')
    log_file.flush()  # Ensure immediate write

# Read system prompt from file
system_prompt_file = 'system_prompt.txt'

log_print(f"Loading system prompt from: {system_prompt_file}")
with open(system_prompt_file, 'r', encoding='utf-8') as f:
    full_prompt = f.read()

# Split into system_prompt (first line or short intro) and context (rest)
# The system_prompt.txt file starts with the documentation, so we'll use it as context
# and add a simple system prompt
system_prompt = "You are a helpful assistant that can hit PrismHR API GET endpoints and return the results based on the user's request/question."
context = full_prompt

def process_query(question: str):
    """Process a single query and return the response"""
    try:
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
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ]
        )

        # MCP tool calls
        log_print("\n--- MCP Tool Calls ---")
        for output_item in resp.output:
            if getattr(output_item, "type", None) == "mcp_call":
                tool_name = output_item.name
                arguments = output_item.arguments
                log_print(f"Tool: {tool_name}")
                log_print(f"Arguments: {arguments}")
        
        log_print("\n--- Response ---")
        log_print(resp.output_text)
        log_print("\n" + "="*80 + "\n")
        
        return resp.output_text
    except Exception as e:
        log_print(f"\n❌ Error processing query: {e}\n")
        import traceback
        import io
        # Capture traceback and write to both terminal and file
        tb_buffer = io.StringIO()
        traceback.print_exc(file=tb_buffer)
        tb_str = tb_buffer.getvalue()
        # Print to terminal
        print(tb_str)
        # Write to file
        log_file.write(tb_str)
        log_file.flush()
        return None

def main():
    """Main interactive loop"""
    # Add session separator to log file
    session_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_print("\n" + "="*80)
    log_print(f"NEW SESSION STARTED: {session_start}")
    log_print("="*80 + "\n")
    
    log_print("="*80)
    log_print("PrismHR MCP Server Test - Interactive Mode")
    log_print("="*80)
    log_print("Type your questions below. Type 'quit' or 'exit' to stop.\n")
    
    while True:
        try:
            # Get user input (don't log the prompt, just the query)
            question = input("Query: ").strip()
            
            # Log the user's query
            log_print(f"Query: {question}")
            
            # Check for quit commands
            if question.lower() in ['quit', 'exit', 'q']:
                log_print("\nGoodbye!")
                break
            
            # Skip empty input
            if not question:
                continue
            
            # Process the query
            process_query(question)
            
        except KeyboardInterrupt:
            log_print("\n\nInterrupted by user. Goodbye!")
            break
        except EOFError:
            log_print("\n\nGoodbye!")
            break
        finally:
            # Ensure file is flushed
            log_file.flush()

if __name__ == "__main__":
    try:
        main()
    finally:
        # Close the log file when done
        log_file.close()

