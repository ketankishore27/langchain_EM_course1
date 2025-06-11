from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents.react.agent import create_react_agent
from langchain import hub
from langchain.agents.agent import AgentExecutor
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain_core.tools import Tool
import os

load_dotenv(override=True)


def run_python_interpretor():
    instruction = """
    You are an agent designed to write and execute python code to answer question.
    You have access to a python REPL, which you can use to execute code.
    If you get an error, debug your code and try again.
    Only use the output of your code to answer question.
    You might know the answer without running any code, but you should still run the code to get an answer.
    If it does not seem like you can write the code to answer question, just return "I don't know" as the answer.
    """

    react_prompt = hub.pull("langchain-ai/react-agent-template").partial(
        instructions=instruction
    )
    tools = [PythonREPLTool()]
    agent = create_react_agent(
        llm=ChatOpenAI(model="gpt-4o"), tools=tools, prompt=react_prompt
    )
    agent_exec = AgentExecutor(agent=agent, max_iteration=3, tools=tools, verbose=True)
    return agent_exec


def get_csv_agent():
    csv_agent = create_csv_agent(
        llm=ChatOpenAI(model="gpt-4o"),
        path=r"rough_work/data/episode_info.csv",
        allow_dangerous_code=True,
        verbose=True,
    )
    return csv_agent


def get_router_agent():

    def get_python_interpretor(original_string):
        return python_execution_agent.invoke({"input": original_string})

    python_execution_agent = run_python_interpretor()
    csv_query_agent = get_csv_agent()
    tool_names = [
        Tool(
            name="Python Code Executor",
            func=get_python_interpretor,
            description="""
            useful when you need to transform natural language to python and execute the python code, 
            returning the results of the code executions. 
            DOES NOT ACCEPT CODE AS INPUT
            """,
        ),
        Tool(
            name="CSV Agent",
            func=csv_query_agent.invoke,
            description="""
            useful when you need to answer question over episode_info.csv file,
            takes an input the entire question and returns the answer after running pandas calculation
            """,
        ),
    ]

    base_prompt = hub.pull("langchain-ai/react-agent-template").partial(instructions="")
    router_agent = create_react_agent(
        llm=ChatOpenAI(model="gpt-4.1"), tools=tool_names, prompt=base_prompt
    )

    route_executor = AgentExecutor(agent=router_agent, tools=tool_names, verbose=True)

    return route_executor


if __name__ == "__main__":
    # python_execution_agent = run_python_interpretor()
    query = """
                    Generate and save in current working directory 2 QrCodes that points to
                    https://www.linkedin.com/in/ketan-kishore-b89643150/. You have the qrcode package already installed
                    Save the files in a folder called as output_qrs
        """
    # result = python_execution_agent.invoke({"input": query})

    # csv_query_agent = get_csv_agent()
    # query = """
    #             "Who wrote the maximum number of episodes"
    #     """
    # result = csv_query_agent.invoke({"input": query})

    route_agent = get_router_agent()
    result = route_agent.invoke({"input": query})
    print(result)
