from dotenv import load_dotenv
load_dotenv()
from agents import Agent
from agents.run_context import RunContextWrapper
from agents.mcp import MCPServerStdio

samples_dir="./samples"
async def main():
    async with MCPServerStdio(params={
        "command":"npx",
        "args":["-y", "@modelcontextprotocol/server-filesystem", samples_dir]
    }) as server:
        run_context=RunContextWrapper(context=None)
        agent=Agent(name="test",instructions="Just testing",model="gpt-5-nano")
        tools=await server.list_tools(run_context,agent)
        for t in tools:
            print(t.name)
            
from agents.mcp import create_static_tool_filter

server = MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
    },
    tool_filter=create_static_tool_filter(
        allowed_tool_names=["read_file", "write_file"]
    )
)

server = MCPServerStdio(
    params={
        "command": "npx", 
        "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
    },
    tool_filter=create_static_tool_filter(
        blocked_tool_names=["delete_file"]
    )
)      
