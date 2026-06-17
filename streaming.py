# ----------------------------Raw response event------------------------------------------
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner
from dotenv import load_dotenv
load_dotenv()

async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
    )

    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())

# ---------------------------Run item events and agent events----------------------------
import asyncio
import random
from agents import Agent, ItemHelpers, Runner, function_tool

@function_tool
def how_many_jokes()->int:
    return random.randint(1,10)


async def main():
    agent=Agent(name='joker',
                instructions="First call the `how_may_jokes` tool, then tell that many jokes.",
                tools=[how_many_jokes],
                model="gpt-4.1-nano")
    result=Runner.run_streamed(agent,input="Hello")
    print("--- Run starting ---")
    async for event in result.stream_events():
        if event.type=="raw_response_event":
            continue
        elif event.type=="agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        elif event.type=="run_item_stream_event":
            if event.item.type=="tool_call_item":
                print("-- Tool was called")
            elif event.item.type=="tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type=="message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass
    print("---Run complete---")

if __name__=="__main__":
    asyncio.run(main())
