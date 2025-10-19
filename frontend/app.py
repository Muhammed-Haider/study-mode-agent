import chainlit as cl
import httpx
from chainlit import AskUserMessage, Message, on_chat_start

API_URL = "http://127.0.0.1:8001/ask"



@cl.on_chat_start
async def start_chat():
    """Initialize the chat session"""


    cl.user_session.set("chat_messages", [])            




@cl.on_message
  
async def on_message(message: cl.Message):
  
    async with httpx.AsyncClient(timeout=60.0) as client:
         chat_messages = cl.user_session.get("chat_messages", [])
         chat_messages.append({"role": "user", "content": message.content})
         response = await client.post(API_URL, json={"text": message.content})
         data = response.json()

         await cl.Message(content=data["answer"]).send()

@cl.on_stop
async def on_stop():
    await cl.Message(content="Paused! Learning is tough, but we can resume whenever you’re ready 😉").send()







  