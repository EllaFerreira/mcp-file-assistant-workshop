"""
MCP File Assistant Server - SOLUTION
A simple MCP server that lets Claude access local files.

This is the complete solution for the workshop exercises.
"""
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
import mcp.server.stdio
import os
from pathlib import Path

# Init the MCP server
app = Server("file-assistant")

# Directory containing files we want to expose
FILES_DIR = Path(__file__).parent.parent / "test_files"


# ============================================================================
# EXERCISE 1: Resources - SOLUTION
# ============================================================================

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List all available text files as resources."""
    import sys
    resources = []
    
    print(f"list_resources called, scanning {FILES_DIR}", file=sys.stderr)
    
    # Get all .txt and .md files from FILES_DIR
    for file_path in FILES_DIR.glob("*.txt"):
        print(f"Found: {file_path.name}", file=sys.stderr)
        resources.append(
            Resource(
                uri=f"file:///{file_path}",
                name=file_path.name,
                mimeType="text/plain",
                description=f"Text file: {file_path.name}"
            )
        )
    
    for file_path in FILES_DIR.glob("*.md"):
        print(f"Found: {file_path.name}", file=sys.stderr)
        resources.append(
            Resource(
                uri=f"file:///{file_path}",
                name=file_path.name,
                mimeType="text/markdown",
                description=f"Markdown file: {file_path.name}"
            )
        )
    
    print(f"Returning {len(resources)} resources", file=sys.stderr)
    return resources


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read the contents of a requested file."""
    import sys
    # Convert URI to string if it's not already
    uri_str = str(uri)
    print(f"read_resource called with URI: {uri_str}", file=sys.stderr)
    
    # Extract the file path from the URI
    file_path = Path(uri_str.replace("file:///", ""))
    print(f"Resolved to path: {file_path}", file=sys.stderr)
    
    # Security check: make sure the file is in FILES_DIR
    if not file_path.is_relative_to(FILES_DIR) and file_path.parent != FILES_DIR:
        # Try to resolve it as just a filename
        file_path = FILES_DIR / file_path.name
    
    # Read and return the file contents
    if file_path.exists():
        content = file_path.read_text()
        print(f"Successfully read {len(content)} characters", file=sys.stderr)
        return content
    else:
        print(f"File not found: {file_path}", file=sys.stderr)
        raise FileNotFoundError(f"File not found: {file_path}")


# ============================================================================
# EXERCISE 3: Tools - SOLUTION
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="read_file",
            description="Read the contents of a text file from the test_files directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to read (e.g., 'notes.txt' or 'todo.md')"
                    }
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="search_files",
            description="Search for text across all files in the test_files directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The text to search for"
                    }
                },
                "required": ["query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "read_file":
        filename = arguments["filename"]
        file_path = FILES_DIR / filename
        
        try:
            if file_path.exists() and file_path.is_file():
                content = file_path.read_text()
                return [TextContent(
                    type="text",
                    text=f"📄 {filename}:\n\n{content}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"File not found: {filename}"
                )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error reading {filename}: {str(e)}"
            )]
    
    elif name == "search_files":
        query = arguments["query"].lower()
        results = []
        
        # Search through all .txt and .md files
        for file_path in list(FILES_DIR.glob("*.txt")) + list(FILES_DIR.glob("*.md")):
            try:
                content = file_path.read_text()
                # Check if query is in the file (case-insensitive)
                if query in content.lower():
                    # Find matching lines
                    matching_lines = []
                    for line_num, line in enumerate(content.split('\n'), 1):
                        if query in line.lower():
                            matching_lines.append(f"  Line {line_num}: {line.strip()}")
                    
                    if matching_lines:
                        result = f"📄 {file_path.name}:\n" + "\n".join(matching_lines)
                        results.append(result)
            except Exception as e:
                results.append(f"Error reading {file_path.name}: {str(e)}")
        
        if not results:
            return [TextContent(
                type="text",
                text=f"No matches found for '{arguments['query']}'"
            )]
        
        return [TextContent(
            type="text",
            text="\n\n".join(results)
        )]
    else:
        raise ValueError(f"Unknown tool: {name}")


# ============================================================================
# Main entry point
# ============================================================================

def main():
    """Run the MCP server."""
    import asyncio
    import sys
    
    try:
        print("Starting MCP File Assistant Server...", file=sys.stderr)
        
        async def run():
            async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
                print("Server streams established", file=sys.stderr)
                await app.run(
                    read_stream,
                    write_stream,
                    app.create_initialization_options()
                )
        
        asyncio.run(run())
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

