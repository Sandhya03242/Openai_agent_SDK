from dotenv import load_dotenv
load_dotenv()
import asyncio
from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, function_tool

@dataclass
class UserInfo:
    name:str
    uid:str

@function_tool
async def fetch_user_age(wrapper:RunContextWrapper[UserInfo])->str:
    """Fetch the age of the user call this function to get users age information."""
    return f"The User {wrapper.context.name} is 47 years old"

async def main():
    user_info=  UserInfo(name="john",uid=123)
    agents=Agent[UserInfo](name="Assistant",tools=[fetch_user_age])
    result=await Runner.run(starting_agent=agents,input="what is the age of the user?", context=user_info)
    print(result.final_output)

if __name__=="__main__":
    asyncio.run(main())