from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import asyncio
import os
from groq import AsyncGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq Client
groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

async def generate_chat_responses(message: str):
    yield "data: [START]\n\n"  # SSE format

    response = await groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": message}],
        stream=True,
    )

    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)  # Print to console in real-time
            yield f"data: {content}\n\n"  # Proper SSE format
            await asyncio.sleep(0.1)  # Allow FastAPI to flush output

    yield "data: [END]\n\n"

@app.get("/chat_stream")
async def chat_stream(message: str = Query(..., description="Chat message")):
    return StreamingResponse(generate_chat_responses(message), media_type="text/event-stream")
