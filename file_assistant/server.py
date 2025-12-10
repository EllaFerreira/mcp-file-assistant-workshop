"""
MCP File Assistant Server
A simple MCP server that lets Claude access local files.

Workshop exercises:
1. Implement list_resources() to show available files
2. Implement read_resource() to read file contents
3. Implement search_files tool to search across files
"""
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
import mcp.server.stdio
from pathlib import Path

# Init the MCP server
app = Server("file-assistant")

# Directory containing files we want to expose
FILES_DIR = Path(__file__).parent.parent / "test_files"


# ============================================================================
# EXERCISE 1: Resources - Let Claude see and read your files
# ============================================================================

@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    List all available text files as resources.
    
    TODO: Implement this function to:
    1. Create an empty list called 'resources'
    2. Use FILES_DIR.glob("*.txt") to find all .txt files
    3. For each file, append a Resource object with:
       - uri: f"file:///{file_path}"
       - name: file_path.name
       - mimeType: "text/plain"
       - description: f"Text file: {file_path.name}"
    4. Do the same for .md files with mimeType="text/markdown"
    5. Return the resources list
    
    Hint: Resource is imported from mcp.types
    """
    
    return []


@app.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read the contents of a requested file.
    
    TODO: Implement this function to:
    1. Convert URI to string: uri_str = str(uri)
    2. Extract the file path: Path(uri_str.replace("file:///", ""))
    3. Security: ensure file is in FILES_DIR by using FILES_DIR / filename
    4. Check if file exists with file_path.exists()
    5. Read and return contents with file_path.read_text()
    6. Raise FileNotFoundError if file doesn't exist
    
    Hint: Path is imported from pathlib
    """
    
    return ""


# ============================================================================
# EXERCISE 2: Tools - Add search functionality
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools.
    
    TODO: Implement this function to:
    1. Return a list containing a Tool object for "search_files"
    2. The Tool should have:
       - name: "search_files"
       - description: "Search for text across all files in the test_files directory"
       - inputSchema: {
           "type": "object",
           "properties": {
             "query": {
               "type": "string",
               "description": "The text to search for"
             }
           },
           "required": ["query"]
         }
    
    BONUS: Add a "read_file" tool to make file reading easier!
       - name: "read_file"
       - description: "Read the contents of a file"
       - inputSchema with "filename" parameter
    
    Hint: Tool is imported from mcp.types
    """
    
    return []


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool calls.
    
    TODO: Implement this function to:
    1. Check if name == "search_files"
    2. Get the query: query = arguments["query"].lower()
    3. Create an empty results list
    4. Loop through all .txt and .md files in FILES_DIR
    5. For each file:
       - Read the content
       - Check if query is in content.lower()
       - Find matching lines with line numbers
       - Format results nicely (e.g., "📄 filename:\n  Line X: content")
    6. Return a TextContent object with the results or "No matches found"
    
    BONUS: Handle the "read_file" tool if you added it!
    
    Hint: TextContent is imported from mcp.types
    """
    
    return [TextContent(type="text", text="Not implemented yet")]


# ============================================================================
# Main entry point - This is already implemented for you my friend!
# ============================================================================

def main():
    """Run the MCP server."""
    import asyncio
    
    async def run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(run())


if __name__ == "__main__":
    main()

