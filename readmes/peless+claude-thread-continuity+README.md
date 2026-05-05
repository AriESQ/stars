# 🧠 Claude Thread Continuity MCP Server

**Never lose context again!** This MCP server automatically saves and restores project state when Claude threads hit token limits, ensuring seamless conversation continuity.

## 🚀 Features

- **🔄 Automatic State Persistence** - Auto-saves project context during conversations
- **⚡ Seamless Restoration** - Instantly restore full context when starting new threads
- **🛡️ Smart Validation** - Prevents project fragmentation with intelligent name checking
- **🔒 Privacy First** - All data stored locally on your machine
- **🎯 Zero Configuration** - Works invisibly once set up
- **📊 Smart Triggers** - Auto-saves on file changes, decisions, milestones
- **🗂️ Multi-Project Support** - Manage multiple concurrent projects

## ✨ NEW: Anti-Fragmentation System

Version 1.1 introduces intelligent project validation to prevent the common issue of accidentally creating multiple similar projects:

- **🔍 Fuzzy Name Matching** - Detects similar project names (70% similarity threshold)
- **⚠️ Validation Warnings** - Suggests consolidation when similar projects exist
- **💪 Force Override** - Bypass validation when genuinely different projects needed
- **🎯 Configurable Thresholds** - Adjust sensitivity for your workflow

### Example Validation in Action

```
❌ Project "Hebrew Speaking Evaluation MVP" blocked
✅ Similar project found: "Hebrew Evaluation MVP" (85% similar)
🎯 Recommendation: Update existing project or use force=true
```

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/peless/claude-thread-continuity.git
cd claude-thread-continuity

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test the enhanced server
python3 test_server.py

# 4. Add to Claude Desktop config
# See setup instructions below
```

## 🛠️ Installation

### 1. Install the MCP Server

```bash
# Create permanent directory
mkdir -p ~/.mcp-servers/claude-continuity
cd ~/.mcp-servers/claude-continuity

# Copy files (or clone repo to this location)
# Place server.py and requirements.txt here
```

### 2. Configure Claude Desktop

Edit your Claude Desktop configuration file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\\Claude\\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "claude-continuity": {
      "command": "python3",
      "args": ["~/.mcp-servers/claude-continuity/server.py"],
      "env": {}
    }
  }
}
```

### 3. Restart Claude Desktop

Close and reopen Claude Desktop. The continuity tools will now be available automatically.

## 🎯 How It Works

### Automatic Context Saving

The server automatically saves project state when:
- ✅ Files are created or modified
- ✅ Technical decisions are made  
- ✅ Project milestones are reached
- ✅ Every 10 messages (fallback)

### Smart Validation Process

Before saving, the system:
1. **Checks for Similar Names** - Uses fuzzy matching to find existing projects
2. **Calculates Similarity** - Compares project names with 70% threshold
3. **Provides Recommendations** - Suggests consolidation or renaming
4. **Allows Override** - Use `force: true` for edge cases

### Context Restoration

When starting a new thread:
1. **Load Project:** `load_project_state: project_name="your-project"`
2. **Full Context Restored:** All technical decisions, files, and progress restored
3. **Continue Seamlessly:** Pick up exactly where you left off

## 🔧 Available Commands

| Command | Description | NEW in v1.1 |
|---------|-------------|-------------|
| `save_project_state` | Save current project state | ✨ Now with validation |
| `load_project_state` | Restore full project context | |
| `list_active_projects` | View all tracked projects | |
| `get_project_summary` | Get quick project overview | |
| `validate_project_name` | Check for similar project names | ✨ NEW |
| `auto_save_checkpoint` | Triggered automatically | |

## 💡 Usage Examples

### Starting a New Project (with Validation)
```
save_project_state: project_name="my-web-app", current_focus="Setting up React components", technical_decisions=["Using TypeScript", "Vite for bundling"], next_actions=["Create header component", "Set up routing"]
```

### Checking Name Before Creating
```
validate_project_name: project_name="my-webapp", similarity_threshold=0.7
```

### Force Override When Needed
```
save_project_state: project_name="my-web-app-v2", force=true, current_focus="Starting version 2"
```

### Continuing After Token Limit
```
load_project_state: project_name="my-web-app"
```

### Viewing All Projects
```
list_active_projects
```

## 🗂️ Data Storage

Project states are stored locally at:
```
~/.claude_states/
├── project-name-1/
│   ├── current_state.json
│   └── backup_*.json
└── project-name-2/
    ├── current_state.json
    └── backup_*.json
```

- **Privacy:** Everything stays on your machine
- **Backups:** Automatic backup rotation (keeps last 5)
- **Format:** Human-readable JSON files
- **Validation:** Metadata tracks validation bypass status

## 🏗️ Project State Structure

Each saved state includes:

```json
{
  "project_name": "my-project",
  "current_focus": "What you're working on now",
  "technical_decisions": ["Key choices made"],
  "files_modified": ["List of files created/changed"],
  "next_actions": ["Planned next steps"],
  "conversation_summary": "Brief context summary",
  "last_updated": "2025-06-15T10:30:00Z",
  "version": "1.1",
  "validation_bypassed": false
}
```

## 🛡️ Validation Configuration

### Default Settings
- **Similarity Threshold:** 70% (0.7)
- **Comparison Method:** Fuzzy string matching
- **Auto-save Behavior:** Bypasses validation (uses `force=true`)

### Customizing Validation
```
validate_project_name: project_name="test-project", similarity_threshold=0.8
```

Higher threshold = stricter matching (0.9 = 90% similar required)
Lower threshold = looser matching (0.5 = 50% similar triggers warning)

## 🔍 Troubleshooting

### Tools Not Appearing
1. Check Claude Desktop logs
2. Verify Python 3 is in your PATH: `python3 --version`
3. Validate JSON config syntax
4. Restart Claude Desktop completely

### Testing the Enhanced Server
```bash
cd ~/.mcp-servers/claude-continuity
python3 test_server.py
```

The test suite now includes validation testing and will report:
- ✅ Basic functionality tests
- ✅ Project validation tests  
- ✅ Fuzzy matching accuracy
- ✅ Force override functionality

### Common Issues

**Validation Too Strict:**
Lower the similarity threshold or use `force=true`

**Permission Errors:**
```bash
chmod +x ~/.mcp-servers/claude-continuity/server.py
```

**Python Path Issues:**
Update the config to use full Python path:
```json
{
  "command": "/usr/bin/python3",
  "args": ["~/.mcp-servers/claude-continuity/server.py"]
}
```

## 🧪 Development

### Requirements
- Python 3.8+
- MCP SDK 1.0+
- difflib (built-in, for fuzzy matching)

### Running Tests
```bash
python3 test_server.py
```

Enhanced test suite includes:
- Basic functionality validation
- **NEW:** Project name similarity testing
- **NEW:** Validation workflow testing
- **NEW:** Force override testing
- **NEW:** MCP tool validation

### Project Structure
```
claude-thread-continuity/
├── server.py           # Main MCP server (enhanced with validation)
├── requirements.txt    # Python dependencies
├── test_server.py     # Comprehensive test suite
├── README.md          # This file
├── LICENSE            # MIT License
└── examples/          # Usage examples
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

### Current Development Priorities
- [ ] Integration with external project management tools
- [ ] Advanced similarity algorithms
- [ ] Project merging utilities
- [ ] Custom validation rules

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🚀 Why This Matters

**Before v1.1:** 😫 Hit token limit → Lose all context → Re-explain everything → Lose momentum

**Common Problem:** 😤 Create "Hebrew MVP", then "Hebrew Evaluation MVP", then "Hebrew Speaking MVP" → Context scattered across multiple projects

**After v1.1:** 😎 Hit token limit → Start new thread → `load_project_state` → Continue seamlessly + Smart validation prevents fragmentation

Perfect for:
- 🏗️ **Complex Development Projects** - Keep track of architecture decisions without fragmentation
- 📚 **Learning & Research** - Maintain context across study sessions with consistent naming
- ✍️ **Writing Projects** - Remember plot points without creating duplicate character projects
- 🔧 **Multi-session Debugging** - Preserve debugging state with clear project organization

## 📈 Version History

### v1.1.0 (Current)
- ✨ **Project Validation System** - Prevents fragmentation with fuzzy name matching
- ✨ **validate_project_name** tool - Manual name checking
- ✨ **Force Override** capability - Bypass validation when needed
- ✨ **Enhanced Testing** - Comprehensive validation test suite
- 🐛 **Bug Fixes** - Improved error handling and edge cases

### v1.0.0
- 🚀 Initial release with core continuity functionality

---

**Built with ❤️ for the Claude community**

*Tired of fragmented projects? Version 1.1 keeps your context organized!*
