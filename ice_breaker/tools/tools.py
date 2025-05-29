from langchain_community.tools import TavilySearchResults

def get_profile_url_tavily(name):
    search_engine = TavilySearchResults()
    results = search_engine.run(f"{name}")
    return results