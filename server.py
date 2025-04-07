from dotenv import load_dotenv
import weave

load_dotenv()

# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("MCP Telemetry")


# Start a new tracing session with Weave
@mcp.tool()
def start_tracing(session_slug: str) -> str:
    """
        Start a new tracing session with Weave using a session slug 
        which will be used to identify the session in Weave. Ideally, 
        the slug will be a short overview of the conversion with all 
        lowercase words separated by hyphens and no more than 10 words.
    """
    weave.init(session_slug)
    return f"Started tracing session with slug: {session_slug}"


# Trace tool
@mcp.tool()
def log_trace(user_input: str, llm_response: str, llm_action: str = None,
             llm_tool_calls: list[str] = None, llm_tool_call_results: list[str] = None,
               llm_tool_call_result_status: list[str] = None) -> str:
    """
        Log a trace of the user input, LLM response, LLM action, LLM tool calls,
        LLM tool call results, and LLM tool call result status to the current tracing session. 
        Only user input and LLM response are mandatory.
    """

    trace = {
        "user_input": user_input,
        "llm_response": llm_response
    }
    
    # Add optional fields if provided
    if llm_action is not None:
        trace["llm_action"] = llm_action
    if llm_tool_calls is not None:
        trace["llm_tool_calls"] = llm_tool_calls
    if llm_tool_call_results is not None:
        trace["llm_tool_call_results"] = llm_tool_call_results
    if llm_tool_call_result_status is not None:
        trace["llm_tool_call_result_status"] = llm_tool_call_result_status
    
    @weave.op()
    def log_trace_op(trace: dict):
        """Log a trace to the current tracing session"""
        return f"Logged trace successfully"
    return log_trace_op(trace)