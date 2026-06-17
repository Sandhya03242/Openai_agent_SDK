import asyncio
from agents import Agent, run_demo_loop
from dotenv import load_dotenv
load_dotenv()

async def main()->None:
    agent=Agent(name="Assistant",instructions="You are a helpful assistant.",model="gpt-5-nano")
    await run_demo_loop(agent)

if __name__=="__main__":
    asyncio.run(main())