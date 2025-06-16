from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import asyncio, os
load_dotenv(".env", override=True)
llm = ChatOpenAI(model="gpt-4o", temperature=0.)

client = MultiServerMCPClient(
        {
            "tools": {
                "command": "python",
                "args": ["/Users/A118390615/Library/CloudStorage/OneDrive-DeutscheTelekomAG/Projects/COE_Projects/langchain_EM_course1/mcp/server/all_tools_merged.py"],
                "transport": "stdio"
            }
        }
    )
        

async def main():
    async with client.session("tools") as session:
        tools = await load_mcp_tools(session)
        agent = create_react_agent(llm, tools)
        result = await agent.ainvoke(
            {"messages": [HumanMessage(content="Get the recent weather alerts for California (CA)")]}
        )

        print ("*" * 10)
        print("Intermediate Calls")
        for rows in result["messages"]:
            print("\n", rows)
        print("*" * 10)

        print ("*" * 10)
        print("Final Answer")
        print(result["messages"][-1].content)
        print("*" * 10)

if __name__ == "__main__":
    asyncio.run(main())
