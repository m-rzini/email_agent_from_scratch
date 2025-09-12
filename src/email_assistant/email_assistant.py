
from langchain.chat_models import init_chat_model

from email_assistant.tools import get_tools, get_tools_by_name
from email_assistant.schemas import RouterSchema



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