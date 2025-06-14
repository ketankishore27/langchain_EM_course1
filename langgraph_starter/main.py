from node import create_reasoning_agent, tool_node
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage
import json
from dotenv import load_dotenv


def create_flow_chart():

    flow = StateGraph(MessagesState)
    flow.add_node("agent_reason", create_reasoning_agent)
    flow.add_node("act", tool_node)
    # flow.add_node("start", START)
    # flow.add_node("end", END)
    flow.add_edge(START, "agent_reason")

    def should_continue(state: MessagesState):
        if state['messages'][-1].tool_calls:
            return "need_to_act"
        
        return "need_to_end"

    flow.add_conditional_edges("agent_reason", should_continue, {
        "need_to_end":END, 
        "need_to_act":"act"}
    )

    flow.add_edge("act", "agent_reason")
    app = flow.compile()
    app.get_graph().draw_mermaid_png(output_file_path = "flow_created.png")
    return app

if __name__ == "__main__":
    load_dotenv(override=True)
    app = create_flow_chart()
    res = app.invoke({"messages": [HumanMessage(content="What is the temperature in Tokyo? List it and then triple it")]})
    with open("response.txt", "w") as f:
        print(res, file = f)

    out_response_onlyAnswer = f"\n\n****\nOutput Response:\n{res["messages"][-1].content}\n\n"
    print(out_response_onlyAnswer)

    out_response_complete = f"\n\n****\nComplete Output:\n{res}\n\n"
    print(out_response_complete)

