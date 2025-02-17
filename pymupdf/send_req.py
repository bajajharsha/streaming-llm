import asyncio

import httpx


async def send_request(pdf_path: str):
    async with httpx.AsyncClient() as client:
        with open(pdf_path, "rb") as f:
            files = {"file": f}
            response = await client.post("http://localhost:8000/upload", files=files)
            # print(response.json())


async def main():
    # Create a list of tasks; here, we're sending 10 concurrent requests
    tasks = [send_request("data/attention.pdf") for _ in range(10)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
