from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import os

load_dotenv(override=True)
llm = ChatOpenAI(model="gpt-4o", temperature=0.)

stdio_server_parameter = StdioServerParameters(
    command="python",
    args=[
        "/Users/A118390615/Library/CloudStorage/OneDrive-DeutscheTelekomAG/Projects/COE_Projects/langchain_EM_course1/mcp/server/math_server.py"
    ]
)

async def main():
    async with stdio_client(stdio_server_parameter) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            tool_list = await session.list_tools()
            tools = await load_mcp_tools(session)
            print(f"Tools Present: {tools}")
            
            agent = create_react_agent(model=llm, tools=tools)
            result = await agent.ainvoke(
                {"messages": [HumanMessage(content="What is 2 + 2")]}
            )
            print(result)

if __name__ == "__main__":
    asyncio.run(main())


# """
# {
#     'messages': [
#                     HumanMessage(content='What is 2 + 2', additional_kwargs={}, response_metadata={}, id='b292fe1f-5ee1-4dcb-9ef4-b87aae08db48'), 
#                     AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_O5QxaeRVQoLNaWb8VNiw6OrA', 'function': {'arguments': '{"num_a":2,"num_b":2}', 'name': 'add'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 19, 'prompt_tokens': 78, 'total_tokens': 97, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_07871e2ad8', 'id': 'chatcmpl-Biz15LJ1RLddHiRRHjld8u9cVBQb6', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run--a42627e8-f349-4893-bfd0-205952f8a1e5-0', tool_calls=[{'name': 'add', 'args': {'num_a': 2, 'num_b': 2}, 'id': 'call_O5QxaeRVQoLNaWb8VNiw6OrA', 'type': 'tool_call'}], usage_metadata={'input_tokens': 78, 'output_tokens': 19, 'total_tokens': 97, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}), 
#                     ToolMessage(content='4.0', name='add', id='2ccafedf-f06e-4453-8224-21dd5bb64803', tool_call_id='call_O5QxaeRVQoLNaWb8VNiw6OrA'), 
#                     AIMessage(content='2 + 2 equals 4.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 9, 'prompt_tokens': 107, 'total_tokens': 116, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_07871e2ad8', 'id': 'chatcmpl-Biz17DgmWRStgBcOyuIJbsU1TDnGQ', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='run--0fbd585c-70c2-4aea-95eb-41f98c184ae4-0', usage_metadata={'input_tokens': 107, 'output_tokens': 9, 'total_tokens': 116, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})
#                 ]
# }

# """