# 🛠️ MCP File Assistant Workshop

**Build your first AI tool in 45 minutes!**

Learn to create a server that lets Claude AI read and search your local files.

## What is MCP?

**Model Context Protocol (MCP)** lets you give Claude AI superpowers! You'll teach Claude to:
- 📁 See your files
- 📖 Read them
- 🔍 Search through them

No complex AI knowledge needed - just 🐍!!!

---

## Before the Workshop

Please install these 3 things:

### 1. Python 3.10+
Check if you have it:
```bash
python --version
```
If not, download from [python.org](https://www.python.org/downloads/)

### 2. uv (Fast Python installer) 

**Mac/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
[UV Tutorial:](https://docs.astral.sh/uv/getting-started/installation/)

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Claude Desktop
- Download: https://claude.ai/download
- Free account required

---

## Setup (5 minutes)

### Step 1: Get the Code
```bash
git clone https://github.com/EllaFerreira/mcp-file-assistant-workshop.git
cd mcp-file-assistant-workshop
```

### Step 2: Install Everything
```bash
# This step creates a virtual environment
uv venv

# Activate it
source .venv/bin/activate     # Mac/Linux
.venv\Scripts\activate        # Windows

# Install dependencies
uv pip install -e .
```

### Step 3: Find Your Full Path
```bash
pwd    # Mac/Linux
cd     # Windows
```
**Copy this path!** You'll need it in the next step ©

### Step 4: Connect to Claude Desktop

Make sure you have Claude Desktop installed, [click here](https://www.claude.com/download).

**Find the config file:**
- **Mac:** Open `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** Open `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** Open `~/.config/Claude/claude_desktop_config.json`

**Add this (replace YOUR_PATH with the path you copied):**

```json
{
  "mcpServers": {
    "file-assistant": {
      "command": "YOUR_PATH/.venv/bin/python",
      "args": [
        "YOUR_PATH/file_assistant/server.py"
      ]
    }
  }
}
```

**Example:**
```json
{
  "mcpServers": {
    "file-assistant": {
      "command": "/Users/yourname/mcp-file-assistant-workshop/.venv/bin/python",
      "args": [
        "/Users/yourname/mcp-file-assistant-workshop/file_assistant/server.py"
      ]
    }
  }
}
```

### Step 5: Restart Claude Desktop
- Quit Claude completely (⌘Q on Mac)
- Open it again
- Look for a 🔌 icon at the bottom - you're connected!

---

## Workshop Exercises

Open `file_assistant/server.py` - this is where you'll code!

### Exercise 1: Let Claude See Your Files (10 min)

**What you'll do:**
- Make Claude list all `.txt` and `.md` files
- Let Claude read them

**Functions to fill in:**
1. `list_resources()` - Show available files
2. `read_resource()` - Read a file

**Hints are in the code!**

---

### Exercise 2: Let Claude Search Files (12 min)

**What you'll do:**
- Create a search tool
- Find text across all files

**Functions to fill in:**
1. `list_tools()` - Define the search tool
2. `call_tool()` - Make search work

**Test it:** Ask Claude "Search for 'workshop' in my files"

---

### Exercise 3: Bonus Challenges

Try adding:
- A tool to read individual files (easier than resources!)
- Support for other file types
- File counting
- Anything else you can think of!

---

## Testing Your Work

After each exercise, test in Claude Desktop:

**Test 1 - Search:**
```
Search for "workshop" in my files
```

**Test 2 - List Files:**
```
What files can you access?
```

**Test 3 - Read a File:**
```
Tell me what's in notes.txt
```

---

## Help! Something's Wrong

### "Server disconnected" Error
This is super common! Try:

1. **Check your paths**
   - Must be full paths (no `~`)
   - Copy-paste them to be sure
   - Example: `/Users/yourname/workshop/...` not `~/workshop/...`

2. **Restart Claude Desktop**
   - Completely quit (⌘Q)
   - Open again

3. **Check the logs**
   ```bash
   tail -f ~/Library/Logs/Claude/mcp.log
   ```
   Look for errors in red

4. **Make sure packages installed**
   ```bash
   cd mcp-file-assistant-workshop
   source .venv/bin/activate
   uv pip install -e .
   ```

### "Can't see files in Claude"
- Did you finish Exercise 1?
- Did you restart Claude after changes?
- Check the 🔌 icon shows your server

### "Tools not showing up"
- Did you finish Exercise 2?
- Restart Claude Desktop
- Tools appear after `list_tools()` is implemented

---

## Project Files

```
mcp-file-assistant-workshop/
├── README.md                 ← You are here
├── file_assistant/
│   ├── server.py            ← Work on this file!
│   └── server_solution.py   ← Peek if stuck
└── test_files/              ← Sample files to test with
    ├── notes.txt
    └── todo.md
```

---

## Stuck? Need Help?

1. **Check the solution:** `file_assistant/server_solution.py`
2. **Ask the instructor** during the workshop
3. **Check MCP docs:** https://modelcontextprotocol.io/

---

## Learn More About MCP

- 📚 [Official MCP Docs](https://modelcontextprotocol.io/)
- 🐍 [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- 💬 [Community Discord](https://discord.com/invite/model-context-protocol-1312302100125843476)
- 🎓 [More Examples](https://github.com/modelcontextprotocol/servers)

---

## After the Workshop

**Want to keep building?**
- Add more file types
- Create tools for other apps
- Share your server with others
- Build something unique!

The MCP community would love to see what you create! 🚀

---

**Built with ❤️ for Build Club Brisbane**

Questions? Open an issue or ask during the workshop!

Happy coding! 👩🏻‍💻
