import asyncio
from agents.realtime import RealtimeAgent, RealtimeRunner
from dotenv import load_dotenv
load_dotenv()
async def main():
    agent=RealtimeAgent(
        name="Assistant",
        instructions="You are a helpful voice assistant. keep your responses conversational and friendly."
    )

    runner=RealtimeRunner(starting_agent=agent,config={
        "model_settings":{
            "model_name":"gpt-4o-mini-realtime-preview-2024-12-17",
            "voice":"alloy",
            "modalities":["text","audio"],
            "input_audio_transcription":{
                "model":"whisper-1"
            },
            "turn_detection":{
                "type":"server_vad",
                "threshold":0.5,
                "prefix_padding_ms":300,
                "silence_duration_ms":200
            }
        }
    })

    session = await runner.run()

    async with session:
        print("Session started! The agent will stream audio responses in real-time.")
        async for event in session:
            if event.type == "response.audio_transcript.done":
                print(f"Assistant: {event.transcript}")
            elif event.type == "conversation.item.input_audio_transcription.completed":
                print(f"User: {event.transcript}")
            elif event.type == "error":
                print(f"Error: {event.error}")
                break
if __name__=="__main__":
    asyncio.run(main())



from agents import function_tool, Agent

@function_tool
def get_weather(city:str)->str:
    """Get current weather for a city."""
    return f"The Weather in {city} in sunny, 72°F"

@function_tool
def book_appointment(date:str, time:str, service:str)->str:
    return f"Appointment booked for {service} on {date} at {time}"

agent=RealtimeAgent(
    name="Assistant",
    instructions="You can help with weather and appointments.",
    tools=[get_weather,book_appointment]
)


from agents.realtime import realtime_handoff

billing_agent=RealtimeAgent(
    name="Billing support",
    instructions="You specialize in billing and payment issues."
)
technical_agent=RealtimeAgent(
    name="Technical support",
    instructions="you handle technical troubleshooting."
)
main_agent=RealtimeAgent(
    name="Customer Service",
    instructions="You are the main customer service agent. Handoff to specialists when needed.",
    handoffs=[
        realtime_handoff(billing_agent,tool_description="Transfer to billing support."),
        realtime_handoff(technical_agent,tool_description="Transfer to technical support")

    ]
)