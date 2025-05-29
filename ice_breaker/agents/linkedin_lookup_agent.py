from dotenv import load_dotenv
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tools import get_profile_url_tavily

def lookup_agent(name: str) -> str:

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    summary_template = """
    Given the full name of the person {name_of_person}, I want you to get me a link to their linkedin profile page.
    Your answer should contain only a url
    """

    prompt_tempate = PromptTemplate(template=summary_template, input_variables=["name_of_person"])

    tools_for_agent = [
        Tool(
            name= "Crawl Google for linkedin pages",
            func= get_profile_url_tavily,
            description= "Useful, when you need to get the LinkedIn Page URL"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke({"input": prompt_tempate.format_prompt(name_of_person=name)})
    print(f"Complete Output Result: {result}")
    linked_profile_result = result["output"]
    return linked_profile_result


if __name__ == "__main__":
    load_dotenv()
    linkedin_url = lookup_agent(name = "Noopur Srivastava Morgan Stanley LinkedIn")
    print(linkedin_url)
