from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from agent import initial_teacher_agent
from agents import Runner
from db import create_table,save_messages,load_messages

app = FastAPI()


@app.on_event("startup")
async def startup():
    await create_table()


class ChatRequest(BaseModel):
    session_id: str
    user_id: str
    messages: list

class Question(BaseModel):
    text:str


@app.post("/ask")
async def ask_question(q: Question):
    result = await Runner.run(initial_teacher_agent, input=q.text)
    return {"answer": result.final_output}

@app.post("/save")
async def save_chat(data: ChatRequest):
    await save_messages(data.session_id, data.user_id, data.messages)
    return {"status": "success"}



@app.get("/load/{session_id}")
async def load_chat(session_id: str):
    messages = await load_messages(session_id)
    return {"messages": messages}