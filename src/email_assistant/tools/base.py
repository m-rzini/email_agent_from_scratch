from typing import Dict, List, Callable, Any, Optional
from langchain_core.tools import BaseTool

def get_tools(tool_names: Optional[List[str]]=None) -> List[BaseTool]:
    """Get specified tools or all tools if tool_names is None.
    
    Args:
        tool_names: Optional list of tool names to include. If None, returns all tools.
        
    Returns:
        List of tool objects
    """

     # Import default tools
    from email_assistant.tools.default.email_tools import write_email, Done, Question
    from email_assistant.tools.default.calendar_tools import schedule_meeting, check_calendar_availability
    
    
    # Base tools dictionary
    all_tools = {
        "write_email" : write_email,
        "Done" : Done,
        "Question" : Question,
        "schedule_meeting" : schedule_meeting,
        "check_calendar_availability" : check_calendar_availability
    }

    # si aucun filtre, retourne tous les outils (dans l'ordre d'insertion)
    if tool_names is None:
        return list(all_tools.values())
    
    # sinon, ne garde que ceux demandés (ignore silencieusement les inconnus)
    return [all_tools[name] for name in tool_names if name in all_tools]

def get_tools_by_name(tools: Optional[List[BaseTool]] = None) -> Dict[str, BaseTool]:
    """Get a dictionary of tools mapped by name."""
    if tools is None:
        tools = get_tools()
    
    return {tool.name: tool for tool in tools}