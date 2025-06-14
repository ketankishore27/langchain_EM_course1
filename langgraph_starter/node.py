from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
from react import llm, tool_list
load_dotenv(override=True)

SYSTEM_MESSAGE = """
You are a helpful AI Assistant who knows how to execute tools
"""

def create_reasoning_agent(state: MessagesState):
    response = llm.invoke([{"role" : "system", "content": SYSTEM_MESSAGE}, *state["messages"]])
    return {"messages": [response]}

tool_node = ToolNode(tool_list)

