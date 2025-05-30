from typing import Any
from langchain.callbacks.base import BaseCallbackHandler

class AgentCallBackHandler(BaseCallbackHandler):

    def on_llm_start(self, serialized, prompts, *, run_id, parent_run_id = None, tags = None, metadata = None, **kwargs) -> Any:
        """ Runs when LLM starts """
        print(f"*** Prompt to LLM was: ***\n{prompts[0]}")
        print("*" * 8)
        return super().on_llm_start(serialized, prompts, run_id=run_id, parent_run_id=parent_run_id, tags=tags, metadata=metadata, **kwargs)


    def on_llm_end(self, response, *, run_id, parent_run_id = None, **kwargs) -> Any:
        """ Runs when LLM ends running """
        print(f"*** LLM Response: ***\n{response.generations[0][0].text}")
        print("*" * 8)
        return super().on_llm_end(response, run_id=run_id, parent_run_id=parent_run_id, **kwargs)

