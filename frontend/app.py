import chainlit as cl
import httpx
API_URL = "http://127.0.0.1:8001/ask"



@cl.on_message
async def main(message: cl.Message):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(API_URL, json={"text": message.content})
        data = response.json()
    # Your custom logic goes here...

    # Send a response back to the user
    await cl.Message(

       content=data["answer"]
        
    ).send()

    # await cl.Message(content=data["answer"]).send()