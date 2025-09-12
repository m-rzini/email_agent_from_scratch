
from typing import Literal

from langchain.chat_models import init_chat_model

from email_assistant.tools import get_tools, get_tools_by_name
from email_assistant.schemas import State, RouterSchema
from email_assistant.prompts import agent_system_prompt, default_background, default_response_preferences, default_cal_preferences
from email_assistant.tools.default import AGENT_TOOLS_PROMPT

from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
load_dotenv(".env")


#Appel des outils
tools = get_tools()
tools_by_name = get_tools_by_name(tools)

# Initialize the LLM for use with router / structured output
llm = init_chat_model("openai:gpt-4.1", temperature=0.0)
llm_router = llm.with_structured_output(RouterSchema) 

# Initialize the LLM, enforcing tool use (of any available tools) for agent
llm = init_chat_model("openai:gpt-4.1", temperature=0.0)
llm_with_tools = llm.bind_tools(tools, tool_choice="any")


#Nodes
def llm_call(state:State):
    """LLM decides whether to call a tool or not"""

    return {
        "messages" : [
            llm_with_tools.invoke(
                [
                    {
                        "role" : "system", "content" : agent_system_prompt.format(
                            tools_prompt = AGENT_TOOLS_PROMPT,
                            background=default_background,
                            response_preferences= default_response_preferences,
                            cal_preferences=default_cal_preferences


                        )
                    }
                ] + state["messages"]
            )
        ]

    }

def tool_node(state:State):
     """Performs the tool call"""
     result = []
     for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append({"role": "tool", "content" : observation, "tool_call_id": tool_call["id"]})
     return {"messages": result}

# Conditional edge function
def should_continue(state: State) -> Literal["Action", "__end__"]:
    """Route to Action, or end if Done tool called"""
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        for tool_call in last_message.tool_calls: 
            if tool_call["name"] == "Done":
                return END
            else:
                return "Action"
            

# Build workflow
agent_builder = StateGraph(State)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("environment", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        # Name returned by should_continue : Name of next node to visit
        "Action": "environment",
        END: END,
    },
)
agent_builder.add_edge("environment", "llm_call")

# Compile the agent
agent = agent_builder.compile()