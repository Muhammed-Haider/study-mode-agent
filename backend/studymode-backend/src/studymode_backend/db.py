import asyncpg
import os
import json
from dotenv import load_dotenv
import asyncpg



load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # Set this in your environment

async def get_conn():
    return await asyncpg.connect(DATABASE_URL)

async def create_table():
    conn = await get_conn()
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS chat_sessions (
        session_id TEXT PRIMARY KEY,
        user_id TEXT,
        messages JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    )
    """)
    await conn.close()

async def save_messages(session_id: str, user_id: str, messages: list):
    conn = await get_conn()
    await conn.execute("""
        INSERT INTO chat_sessions(session_id, user_id, messages)
        VALUES($1, $2, $3)
        ON CONFLICT (session_id) DO UPDATE SET messages=$3
    """, session_id, user_id, json.dumps(messages))
    await conn.close()

async def load_messages(session_id: str):
    conn = await get_conn()
    row = await conn.fetchrow(
        "SELECT messages FROM chat_sessions WHERE session_id=$1",
        session_id
    )
    await conn.close()
    return row["messages"] if row else []
