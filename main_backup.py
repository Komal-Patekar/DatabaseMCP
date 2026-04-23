from fastmcp import FastMCP
from db import call_procedure
from ratelimiter import check_rate_limit

mcp = FastMCP("MCP_Demo")

@mcp.tool()
def add(a: int, b:int) -> int:
    """ Add two integer numbers """
    return a+b

@mcp.tool()
def square(a: int) -> int:
    """ Get square of a number """
    return a*a

@mcp.tool()
def greet(name: str) -> str:
    """ Greet a person """
    return f"Hello {name}"

@mcp.tool
def get_recent_users():
    """ Get list of mysql users """
    check_rate_limit()
    return call_procedure("get_recent_users")

if __name__ == "__main__":
    mcp.run()
