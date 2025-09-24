from agents import Agent
from agents import Runner
from agents import OpenAIChatCompletionsModel
from agents import set_default_openai_client
import os
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI
from openai import AsyncOpenAI

# 0.1. Loading the environment variables
load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","AIzaSyAkw4-LD1vmPYUmgb5XirLgJz0UXCTbWy4")




external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)



llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)


math_agent = Agent(
    name="Math Tutor",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    model=llm_model
)
# set_default_openai_client(external_client)


async def main():
    result = await Runner.run(math_agent, "Why is Linear ALgebra used?")
    print(result.final_output)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
