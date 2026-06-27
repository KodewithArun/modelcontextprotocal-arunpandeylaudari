import threading
import uvicorn
from fastmcp import FastMCP
from app import app

FASTAPI_PORT = 8765

mcp = FastMCP.from_fastapi(
    app,
    name="expenses-tracker"
)

if __name__ == "__main__":
    mcp.run(transport="stdio")