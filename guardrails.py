from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
load_dotenv()
from agents import Agent,  GuardrailFunctionOutput, InputGuardrailTripwireTriggered, RunContextWrapper, Runner, TResponseInputItem, input_guardrail

class MathHomeOutput(BaseModel):
    is_math_homework:bool
    reasoning:str

guardrail_agent=Agent(name="Guardrail check", instructions="check if the user is asking you to do their math homework",
                      output_type=MathHomeOutput,model="gpt-5-nano")
@input_guardrail
async def math_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_math_homework,
    )


agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],model="gpt-5-nano"
)

async def main():
    try:
        await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
        print("Guardrail didn't trip - this is unexpected")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

if __name__=="__main__":
    asyncio.run(main())