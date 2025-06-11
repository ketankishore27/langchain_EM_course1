from typing import Tuple
from functools import partial
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup_agent
from dotenv import load_dotenv
from output_parser import summary_parser, Summary


def ice_break_with(name: str) -> Tuple[Summary, str]:

    linkedin_url = lookup_agent(name)
    linkedin_text = scrape_linkedin_profile(linkedIn_url=linkedin_url, mock=False)

    summary_template = """
    given the information {information} about a person from I want you to create:
    1. a short summary
    2. two intersting facts about them

    \n{format_instruction}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instruction": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    chain = summary_prompt_template | llm | summary_parser
    res: Summary = chain.invoke(input={"information": linkedin_text})

    return res, linkedin_text.get("photoUrl")


if __name__ == "__main__":

    load_dotenv()
    print("Ice Breaker Enter")
    result_set, photo_url = ice_break_with("Noopur Srivastava Morgan Stanley LinkedIn")
    print(result_set, photo_url)
