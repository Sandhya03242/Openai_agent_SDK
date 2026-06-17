# from agents import Agent, handoff
# billing_agent=Agent(name="Billing agent",model="gpt-5-nano")
# refund_agent=Agent(name="Refund agent",model="gpt-5-nano")

# triage_agent=Agent(name="Triage agent",handoffs=[billing_agent, handoff(refund_agent)])


# -----------------------------------------------------------------------------------------

# from agents import Agent, handoff, RunContextWrapper

# def on_handoff(ctx: RunContextWrapper[None]):
#     print("Handoff called")

# agent=Agent(name="My agent")
# handoff_obj=handoff(agent=agent, on_handoff=on_handoff, tool_description_override="custom_handoff_tool")


# --------------------------------------------------------------------

# from agents import Agent, handoff
# from agents.extensions import handoff_filters
# agent=Agent(name="FAQ agent")
# handoff_obj=handoff(agent=agent,input_filter=handoff_filters.remove_all_tools)


# --------------------------------------------------------------------------------
# from agents import Agent
# from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

# billing_agent = Agent(
#     name="Billing agent",
#     instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
#     <Fill in the rest of your prompt here>.""",
# )

# ------------------------------------------------------------------------------

from agents import Agent, Runner, trace
import asyncio
from dotenv import load_dotenv
load_dotenv()
async def main():
    agent=Agent(name="Joke generator",instructions="Tell funny jokes",model="gpt-5-nano")
    with trace("joke workflow"):
        first_result=await Runner.run(agent,"Tell me a joke.")
        second_result=await Runner.run(agent,f"Rate tis joke {first_result.final_output}")
        print(f"joke: {first_result.final_output}")
        print(f"rate: {second_result.final_output}")
if __name__=="__main__":
    asyncio.run(main())