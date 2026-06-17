from agents import Agent, Runner, Session,  SQLiteSession
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    agent=Agent(name="Assistant",instructions="Reply very concisely.",model="gpt-4.1-nano")
    session=SQLiteSession("conversation_123","conversations_history.db")
    print("-----session Example--------")
    print("First turn: ")
    print("user: What City is the Golden Gate Bridge in?")
    result=await Runner.run(agent,"What City is the Golden Gate Bridge in?",session=session)
    print("result: ", result.final_output)
    print()
    print("second turn: ")
    print("user: what state is it in?")
    result=await Runner.run(agent,"what state is it in?",session=session)
    print("result: ", result.final_output)
    print()
    print("third turn: ")
    print("user: What is the population of that state")
    result=await Runner.run(agent,"What is the population of that state",session=session)
    print("result: ", result.final_output)

if __name__=="__main__":
    asyncio.run(main())
