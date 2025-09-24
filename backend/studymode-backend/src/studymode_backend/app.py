from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from agent import math_agent
from agents import Runner

app = FastAPI()

class Question(BaseModel):
    text: str

@app.post("/ask")
async def ask_question(q: Question):
    result = await Runner.run(math_agent, input=q.text)
    return {"answer": result.final_output}
