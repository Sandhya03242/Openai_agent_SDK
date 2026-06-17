# from agents import Agent, Runner,OpenAIChatCompletionsModel,AsyncOpenAI, ModelSettings
# import asyncio
# from dotenv import load_dotenv
# load_dotenv()
# spanish=Agent(
#     name="spanish agent",
#     instructions="You only speak Spanish.",
#     model="gpt-5-nano"
# )
# english_agent = Agent(
#     name="English agent",
#     instructions="You only speak English",
#     model=OpenAIChatCompletionsModel( 
#         model="gpt-5-nano",
#         openai_client=AsyncOpenAI()
#     ),
# )

# triage_agent=Agent(
#     name="Triage agent",
#     instructions="Handoff to the appropriate agent based on the language of the request.",
#     handoffs=[spanish,english_agent],
#     model="gpt-5-nano"
# )

# async def main():
#     result=await Runner.run(triage_agent,"Hola, ¿cómo estás? in English")
#     print(result.final_output)

# if __name__=="__main__":
#     asyncio.run(main())



# english_agent=Agent(name="English agent", instructions="you only speak english",model="gpt-5-nano",model_settings=ModelSettings(temperature=0.1,extra_args={"service_tier": "flex", "user": "user_12345"}))



# ----------------------------LiteLLM------------------------------------------------


from __future__ import annotations

import asyncio

from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
import os

@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main(model: str="gpt-5-nano", api_key: str=os.environ.get("OPENAI_API_KEY")):
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=LitellmModel(model=model, api_key=api_key),
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)


if __name__ == "__main__":
    # First try to get model/api key from args
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=False)
    parser.add_argument("--api-key", type=str, required=False)
    args = parser.parse_args()

    model = args.model
    if not model:
        model = input("Enter a model name for Litellm: ")

    api_key = args.api_key
    # if not api_key:
    #     api_key = input("Enter an API key for Litellm: ")

    asyncio.run(main(model, api_key))