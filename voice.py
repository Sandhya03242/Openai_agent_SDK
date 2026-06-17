import numpy as np
import sounddevice as sd
from agents.voice import AudioInput
import asyncio
import random
from agents import Agent, function_tool
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from agents.voice import SingleAgentVoiceWorkflow, VoicePipeline
from dotenv import load_dotenv
load_dotenv()

@function_tool
def get_weather(city:str)->str:
    """Get the weather for a given city."""
    print(f"[debug] get_weather called with city: {city}")
    choices=["sunny","cloudy","rainy","snowy"]
    return f"The Weather in {city} is {random.choice(choices)}."

english_agent=Agent(
    name="English Agent",
    handoff_description="A english speaking agent.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and "
    ),
    model="gpt-5-nano"
)

agent=Agent(
    name="Assistant",
    instructions=prompt_with_handoff_instructions("You're speaking to a human, so be polite and concise. if the user speak in english, handoff to the english agent."),
    model="gpt-5-nano",
    handoffs=[english_agent],
    tools=[get_weather]
)

async def main():
    pipeline=VoicePipeline(workflow=SingleAgentVoiceWorkflow(agent))
    buffer=np.zeros(24000*3,dtype=np.int16)
    audio_input=AudioInput(buffer=buffer)
    result=await pipeline.run(audio_input)

    player=sd.OutputStream(samplerate=24000, channels=1, dtype=np.int16)
    player.start()

    async for event in result.stream():
        if event.type=="voice_stream_event_audio":
            player.write(event.data)

if __name__=="__main__":
    asyncio.run(main())