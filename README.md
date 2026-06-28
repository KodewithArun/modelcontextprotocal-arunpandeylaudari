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
