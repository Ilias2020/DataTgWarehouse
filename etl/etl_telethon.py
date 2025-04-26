# etl/etl_telethon.py

from telethon import TelegramClient
import psycopg2
import asyncio
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

SESSION_PATH = '../sessions/my_session'

DB_HOST = 'localhost'
DB_PORT = 5433
DB_NAME = 'tgwarehouse'
DB_USER = 'postgres'
DB_PASSWORD = '123321'

CHANNEL = 'telegram'

async def main():
    print(f"API_ID: {API_ID}")
    print(f"API_HASH: {API_HASH}")

    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    await client.start()

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    async for message in client.iter_messages(CHANNEL, limit=100):
        if message.text:
            cur.execute(
                """
                INSERT INTO events (channel_name, message_id, text, views, timestamp, tags, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (channel_name, message_id) DO NOTHING;
                """,
                (
                    CHANNEL,
                    message.id,
                    message.text,
                    message.views or 0,
                    message.date,
                    [],
                    'telegram'
                )
            )
            conn.commit()

    cur.close()
    conn.close()
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
