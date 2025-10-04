from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import logging
import sys
import debugpy
import os
from mcp.server.fastmcp.resources import FileResource
from mcp.server.fastmcp.server import Context
from setup import RESULTS_DATE_PATH    
debugpy.listen(("localhost", 5678))


from extract_data_from_cleaned_response import ParseMarkdownFiles

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("weather")



@mcp.resource("data://funeral_director_names")
def GetFuneralDirectorNames() -> list[str]:
    """
    Get list of funeral directors. These correspond to the funeral directors (companies) 
    whose data we want to process


    Returns:
    List[str]: The list of funeral director names

    Example: ['Hautauspalvelu Kielonkukka', 'HOK Elanto', ...]
    """

    
    FUNERAL_DIRECTOR_NAMES = [x for x in os.listdir(RESULTS_DATE_PATH) if x != "cleaned"]

    return FUNERAL_DIRECTOR_NAMES


@mcp.resource("data://{fd_name}/price_information")
def GetFuneralDirectorResults(fd_name) -> str:
    """
    Get price information for a specific funeral director.
    
    Args:
        fd_name: The name of the funeral director
    
    Returns:
        str: JSON string containing the price information
    """
    file_path = f"{RESULTS_DATE_PATH}/{fd_name}/prices_raw_2.json"
    
    # Read and return the file contents
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return content

@mcp.tool()
async def GetFuneralDirectorResults(fd_name: str, ctx : Context) -> str:
    """
    Get price information for a specific funeral director.
    
    Args:
        fd_name: The name of the funeral director
    
    Returns:
        str: JSON string containing the price information
    """
    # Read the Price information as resource
    content_list = await ctx.read_resource(f"data://{fd_name}/price_information")

    content = content_list[0].content

    return content



@mcp.tool()
async def ExtractFuneralPriceInformation(fd_name : str) -> None:
    """
    Process raw price file for a funeral company to extract prices.
    The function writes the results to a file.  
    
    
    
    Args:  
      fd_name: the funeral director name

    Returns:

    """

    try:
        ParseMarkdownFiles(fd_name)
        
    except Exception as e:
        logger.error(f"Error msg: {e}")



if __name__ == "__main__":
   try:
      mcp.run(transport = "stdio")    
   except Exception as e:
      print(e, file = sys.stderr)
   

   

