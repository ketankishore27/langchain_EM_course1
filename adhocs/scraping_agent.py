from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.output_parsers.json import JsonOutputParser
from langchain.tools.render import render_text_description

import pandas as pd
import requests 
import os
from dotenv import load_dotenv
import time

@tool
def scrape_website_table(url: str) -> int:
    """
        This function scrapes website and return only the html table section
    """
    attempt = 0
    response_code = None
    while (response_code != 200) | (attempt == 3):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
            response = requests.get(url, timeout = 10, headers=headers)
            response.raise_for_status()
            response_code = response.status_code
            if response_code!= 200:
                print("Inside scrape_website, Retrying to scrape")
            soup = BeautifulSoup(response.text, "html.parser")
            tables = soup.find_all("table")
            full_text = " ".join([table.get_text() for table in tables])
            print("\n\nInside scrape_website, Returning scraped source_code\n\n")
            return full_text
        except Exception as e:
            print("Inside scrape_website, Error fetching the content", e)
            return " "
        
        attempt += 1


def find_function(tool_list, tool_name):
    for tool_func in tool_list:
        if tool_name == tool_func.name:
            return tool_func

    raise ValueError("No Such tool found")

def setlogs(sample_agent, step):

    print("*"*8, f"Step{step}", "*"*8)
    print(sample_agent)
    print("*"*8, "End", "*"*8, "\n\n")

def write_to_disk(sample_data, key="table"):
    data = pd.DataFrame(sample_data)
    time_identifier = str(round(int(time.time())))
    path = f"output_data/{key}_{time_identifier}.csv"
    data.to_csv(path, index=False)
    print(f"\n\nOutput file at {path}\n\n")
    return data

def get_dataframe(dict_sample):
    response, data = dict_sample['Final Answer'], ""
    if isinstance(response, dict):
        response_keys = response.keys()
        try:
            for key in response_keys:
                dict_df = response[key]
                data = write_to_disk(dict_df, key)
                time.sleep(1)
        except Exception as e:
            print("This exception")
            print(f"Error Occured in parsing the results for {key}")
        
    elif isinstance(response, list):
        try:
            data = write_to_disk(response)
        except Exception as e:
            print(f"Error Occured in parsing the results", e)

    else:
        pass
            
    return data


def play_with_agent(user_prompt: str):
    react_prompt = """
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
    Return the response and `Final Answer` only in json format.
    If there is a table, return the table in json format

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    """
    tools = [scrape_website_table]
    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    prompt = PromptTemplate.from_template(react_prompt, 
                                        partial_variables = {"tools" : render_text_description(tools), 
                                                            "tool_names" : ", ".join([t.name for t in tools])}
                                        )

    agent = (
        {
            "input" : lambda x: x["input"],
            "agent_scratchpad": lambda x: x["agent_scratchpad"]
        }
        | prompt
        | llm
        | JsonOutputParser()
    )

    agent_step, intermediate_step, step = "", [], 0
    while ("Final Answer" not in agent_step):

        observation = None
        agent_step = agent.invoke(
            {
                "input": user_prompt,
                "agent_scratchpad": intermediate_step
            }
        )
        step += 1
        setlogs(agent_step, step)

        if ("Action" in agent_step) and ("Action Input" in agent_step):
            tool_name = agent_step['Action']
            tool_input = agent_step['Action Input']
            tool = find_function(tools, tool_name)
            observation = tool.func(tool_input)

        if observation:
            intermediate_step.append([agent_step, observation])
        else:
            intermediate_step.append([agent_step])      


    get_dataframe(agent_step)

if __name__ == "__main__":
    load_dotenv()
    user_prompt = "Extract me the table from URL: https://cleartax.in/s/cost-inflation-index"
    play_with_agent(user_prompt)
    #user_prompt = "Extract me the table from URL: https://www.bls.gov/schedule/news_release/ppi.htm#"
    #user_prompt = "Extract me the table from URL: https://www.bls.gov/schedule/news_release/cpi.htm#"
    #user_prompt = "Extract me the table from URL: https://www.morningstar.com/asset-management-companies/morgan-stanley-BN000009H1/funds"
    #user_prompt = "Extract me the table from URL: https://tradingeconomics.com/india/inflation-cpi"
    #user_prompt = "Extract me the table from URL: https://tradingeconomics.com/country-list/inflation-rate"
    #user_prompt = "Extract me the table from URL: https://cleartax.in/s/cost-inflation-index"
