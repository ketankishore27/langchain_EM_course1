from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain_core.tools import tool
load_dotenv(override=True)

@tool
def multiply_number_3(number: float) -> float:
    """
    This function accepts a number, multiplies it by 3 and returns the results
    Args:
        number: number which needs to be multiplied
    Returns:
        number multiplies by 3
    """
    return number * 3

search_tool = TavilySearchResults()

tool_list = [search_tool, multiply_number_3]

llm = ChatOpenAI(model="gpt-4o", temperature=0.).bind_tools(tool_list)
