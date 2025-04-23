# server.py
# This is a simple example of a FastMCP server that provides a tool to place buy/sell orders.

from mcp.server.fastmcp import FastMCP
from index import placebuyorder,placesellorder
# Create an MCP server

mcp = FastMCP("trade")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def buyorder(symbolname:str,qty:int,limit_price:float,exchange:str):
   """Place a buy order"""
   return placebuyorder(symbolname,qty,limit_price,exchange)

@mcp.tool()
def sellorder(symbolname:str,qty:int,limit_price:float,exchange:str):
   """Place a sell order"""
   return placesellorder(symbolname,qty,limit_price,exchange)
   
if __name__=="__main__":
    # Run the server
    mcp.run()   
    
    
# sellorder("HDFCBANK",1,1800,"NSE")