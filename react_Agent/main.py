from dotenv import load_dotenv
from typing import Union, List
from langchain_core.tools import tool, Tool
from langchain_core.prompts import PromptTemplate
from langchain.tools.render import render_text_description
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser
from langchain.agents.output_parsers.react_single_input import (
    ReActSingleInputOutputParser,
)
from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents.format_scratchpad.log import format_log_to_str
from callbacks import AgentCallBackHandler

@tool
def get_text_length(text: str) -> int:
    """
    Return the length of a text by characters
    """
    text = text.strip("'\n").strip('"')
    return len(text)


def find_tool(tools: List[Tool], tool_name: str):
    for tool in tools:
        if tool.name == tool_name:
            return tool

    raise ValueError("The tool was not found.")


if __name__ == "__main__":
    print("Hello LangChain")
    load_dotenv()
    tools = [get_text_length]

    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join(t.name for t in tools),
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini", stop=["\nObservation", "Observation"], temperature=0, callbacks=[AgentCallBackHandler()]
    )
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )
    intermediate_steps = []
    agent_step = ""
    while not isinstance(agent_step, AgentFinish):
        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {   
                "input": "What is the text length of 'DOG' in charaters?", 
                "agent_scratchpad": intermediate_steps
            }
        )
        print(f"Agent Step: {agent_step}")

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_input = agent_step.tool_input
            tool = find_tool(tools, tool_name)
            result = tool.func(tool_input)
            intermediate_steps.append([agent_step, str(result)])

    
    if isinstance(agent_step, AgentFinish):
        print(agent_step.return_values)

