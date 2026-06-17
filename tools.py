# --------------Host tool----------------------------------------
# import asyncio
# from agents import Agent, FileSearchTool, WebSearchTool, Runner
from dotenv import load_dotenv
load_dotenv()
# agent=Agent(name="Assistant",
#             tools=[WebSearchTool()],
#             model="gpt-5-nano")
# async def main():
#     result=await Runner.run(agent,"what is the weather in Malappuram and best cafe in edappal")
#     print(result.final_output)


# if __name__=="__main__":
#     asyncio.run(main())


# ----------------function tool-------------------------------------

# import json
# from typing_extensions import TypedDict, Any
# from agents import Agent , FunctionTool, RunContextWrapper, function_tool

# class Location(TypedDict):
#     lat: float
#     long: float

# @function_tool
# async def fetch_weather(location:Location)->str:
#     """Fetch the weather for a given location.

#     Args:
#         location: The location to fetch the weather for.
#     """
#     return "sunny"

# @function_tool(name_override="fetch_data")
# def read_file(ctx:RunContextWrapper[Any],path:str,directory:str|None=None)->str:
#     """Read the contents of a file.

#     Args:
#         path: The path to the file to read.
#         directory: The directory to read the file from.
#     """
#     return "<file contents>"
# agent=Agent(name="Assistant",tools=[fetch_weather,read_file],model="gpt-5-nano")
# for tool in agent.tools:
#     if isinstance(tool,FunctionTool):
#         print(tool.name)
#         print(tool.description)
#         print(json.dumps(tool.params_json_schema,indent=2))
#         print()

# --------------------custom function tool-----------------------
# from agents import FunctionTool, RunContextWrapper
# from pydantic import BaseModel
# from typing import Any

# def do_some_work(data:str)->str:
#     return "done"

# class FunctionArgs(BaseModel):
#     username:str
#     age:str

# async def run_function(ctx: RunContextWrapper[Any], args:str)->str:
#     parsed = FunctionArgs.model_validate_json(args)
#     return do_some_work(data=f"{parsed.username} is {parsed.age} years old")

# tool= FunctionTool(name="process_user",description="Processes extracted user data",params_json_schema=FunctionArgs.model_json_schema(),on_invoke_tool=run_function)
# print(tool.name)

# --------------------Agents as tools--------------------------------

# from agents import Agent, Runner
# import asyncio

# spanish_agent=Agent(
#     name="Spanish agent",model="gpt-5-nano",
#     instructions="You translate the user's message to spanish"
# )

# french_agent=Agent(
#     name="French agent", model="gpt-5-nano",
#     instructions="You translate the user's message to french"
# )

# orchestrator_agent=Agent(
#     name="orchestrator_agent",
#     instructions=(
#         "You are a translation agent. You use the tools given to you to translate."
#         "If asked for multiple translations, you call the relevant tools."
#     ),model="gpt-5-nano",
#     tools=[
#         spanish_agent.as_tool(
#             tool_name="translate_to_spanish",
#             tool_description="Translate the user's message to spanish"
#         ),
#         french_agent.as_tool(
#             tool_name="translate_to_french",
#             tool_description="Translate the user's message to french"
#         )
#     ]
# )

# async def main():
#     result=await Runner.run(orchestrator_agent, input="Say 'Hello, how are you?' in french")
#     print(result.final_output)

# if __name__=="__main__":
#     asyncio.run(main())


# -----------------------conditional tool enabling------------------------------------------

import asyncio
from agents import Agent, AgentBase, Runner, RunContextWrapper
from pydantic import BaseModel

class LanguageContext(BaseModel):
    Language_preference:str="french spanich"

def french_enabled(ctx:RunContextWrapper[LanguageContext],agent: AgentBase)->bool:
    """Enable French for French+Spanish preference."""
    return ctx.context.Language_preference=="french_spanich"

spanish_agent=Agent(
    name="spanish_agent",
    instructions="You respond in Spanish. Always reply to the user's question in Spanish.",
    model="gpt-5-nano"
)

french_agent=Agent(
    name="french_agent",
    instructions="You respond in french. Always reply to the user's question in french.",
    model="gpt-5-nano"
)
spanish_tool=spanish_agent.as_tool(
            tool_name="respond_spanish",
            tool_description="Respond to the user's question in Spanish",
        )
spanish_tool.is_enabled=True
french_tool=french_agent.as_tool(
            tool_name="respond_french",
            tool_description="Respond to the user's question in French",
        )
french_tool.is_enabled=french_enabled

orchestrator = Agent(
    name="orchestrator",
    instructions=(
        "You are a multilingual assistant. You use the tools given to you to respond to users. "
        "You must call ALL available tools to provide responses in different languages. "
        "You never respond in languages yourself, you always use the provided tools."
    ),
    tools=[
        spanish_tool,
        french_tool
    ]
)

async def main():
    context=RunContextWrapper(LanguageContext(Language_preference="french_spanish"))
    result=await Runner.run(orchestrator,"How are you?",context=context.context)
    print(result.final_output)

asyncio.run(main())



