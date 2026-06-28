# Expense Tracker MCP Server

An MCP (Model Context Protocol) server for tracking expenses, built with FastMCP and SQLite.

## Tools

| Tool | Description |
|------|-------------|
| `add_expense` | Add a new expense (amount, category, description, date) |
| `list_expenses` | List expenses with optional filters (category, date range) |
| `get_expense` | Get a single expense by ID |
| `update_expense` | Update amount, category, description, or date |
| `delete_expense` | Delete an expense by ID |
| `get_summary` | Total, count, average, breakdown by category |
| `get_expenses_by_category` | Group all expenses by category |

## Resources

- `expenses://summary` — Overall expense summary
- `expenses://category/{category}` — Expenses for a specific category

## Categories

Food, Transport, Shopping, Entertainment, Bills, Healthcare, Education, Other

## Local Development

```bash
uv run main.py
```

The server starts at `http://0.0.0.0:8080/mcp`.

## Claude Code (Remote — hosted on Render)

Add as a project-scoped server (creates `.mcp.json` in the repo root):

```bash
claude mcp add --scope project --transport sse expense-tracker https://modelcontextprotocal-arunpandeylaudari.onrender.com/mcp
```

Or add manually to `.mcp.json`:

```json
{
  "mcpServers": {
    "expense-tracker": {
      "type": "sse",
      "url": "https://modelcontextprotocal-arunpandeylaudari.onrender.com/mcp"
    }
  }
}
```

## Claude Code (Local dev)

```bash
claude mcp add --scope project expense-tracker -- uv run main.py
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "expense-tracker": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "main.py"]
    }
  }
}
```

## OpenCode Config

```json
{
  "mcp": {
    "expense-tracker": {
      "type": "local",
      "command": ["uv", "run", "main.py"]
    }
  }
}
```
```
