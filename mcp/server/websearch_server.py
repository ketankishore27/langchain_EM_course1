import httpx
from bs4 import BeautifulSoup
import os
from mcp.server.fastmcp import FastMCP
import asyncio
from dotenv import load_dotenv
load_dotenv(".env", override=True)

mcp = FastMCP(name = "search_tool")

async def scrape_website(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout = 10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            paragraph = soup.find_all("p")
            full_text = " ".join([p.get_text() for p in paragraph])
            return full_text
        except Exception as e:
            print("Error fetching the content", e)
            return " "

async def format_search_results(json_body: dict, num_results = 3):
    result_list = []
    for result in json_body["organic"][:num_results]:
        link = result.get('link', "unknown")
        if link != "unknown":
            scraped_text = await scrape_website(link)
            
        result_body = f"""
        Title: {result.get('title', "unknown")}
        Link: {link}
        Snippet: {result.get('snippet', "unknown")}
        Full_text: {scraped_text}
        """
        result_list.append(result_body)

    return "\n -- \n".join(result_list)

@mcp.tool()
async def get_google_search(query: str, num_results_ent: int) -> str:
    """
        Make Request to make a google search
    
    """

    headers = {
      'X-API-KEY': os.getenv("SERPER_API_KEY"),
      'Content-Type': 'application/json'
    }

    payload = {
        "q": query
    }
    SERPER_API_URL = "https://google.serper.dev/search"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(SERPER_API_URL, headers=headers, json = payload)
            response.raise_for_status()
            final_text = await format_search_results(response.json(), num_results = num_results_ent)
            return final_text
        except Exception as e:
            print(e)
            return e 

if __name__ == "__main__":
    mcp.run(transport="stdio")
    # sample_result = asyncio.run(get_google_search(query = "What is the news about Operation Sindoor", num_results_ent=3))
    # print(sample_result)



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