from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain.agents.agent import AgentExecutor
from langchain_core.tools import tool
from langchain import hub


@tool
def multiply(a: float, b: float) -> float:
    """
    Helps in multiplying two numbers
    """
    return a * b


def create_Agent():
    tools = [TavilySearchResults(), multiply]

    # prompt = hub.pull("langchain-ai/react-agent-template").partial(instructions = "",
    #                                                                tools = tools,
    #                                                                tool_names = ", ".join([i.name for i in tools]))

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_tool_calling_agent(
        llm=ChatOpenAI(model="gpt-4o-mini"), tools=tools, prompt=prompt
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


if __name__ == "__main__":
    load_dotenv(override=True)
    agent_exec = create_Agent()
    # result = agent_exec.invoke({
    #     "input": "Multiply the numbers 3 and 2"
    # })

    result = agent_exec.invoke(
        {"input": "What is the weather update for Mumbai and Washington"}
    )
    print(result)
