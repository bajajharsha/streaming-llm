from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import asyncio
import os
import groq
from groq import AsyncGroq
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize Groq Client
groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

async def generate_chat_responses(message: str):
    yield "[START]\n"

    response = await groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": message}],
        stream=True,
    )

    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)  # Print in real-time
            yield f"{content}\n"
            # await asyncio.sleep(0)  # Allow FastAPI to flush output

    yield "\n[END]\n"

@app.get("/chat_stream")
async def chat_stream(message: str = Query(..., description="Chat message")):
    return StreamingResponse(generate_chat_responses(message), media_type="text/plain")
