from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def fake_video_streamer():
    yield "data: [START]\n\n"
    for i in range(10):
        yield f"data: frame {i}\n\n"
        await asyncio.sleep(1)
    yield "data: [END]\n\n"

@app.get("/video")
async def video():
    return StreamingResponse(fake_video_streamer(), media_type="text/event-stream")
