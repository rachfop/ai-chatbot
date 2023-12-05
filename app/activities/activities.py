import logging
import os
from dataclasses import dataclass
from typing import Optional

import aiohttp
from dotenv import load_dotenv
from temporalio import activity

from .helpers import escape_markdown

load_dotenv()
KAPA_API_ENDPOINT = os.getenv("KAPA_API_ENDPOINT")
KAPA_API_TOKEN = os.getenv("KAPA_API_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


@dataclass
class BotParams:
    message: str
    chat_id: int


@activity.defn
async def send_start_message(input: BotParams) -> str:
    activity.heartbeat("Starting the bot")
    return f"Hello, I am Temporal's Chatbot\. I can answer questions about Temporal\. Please ask me a question\!"


@activity.defn
async def process_and_respond(input: BotParams) -> str:
    activity.heartbeat("Processing the request")
    kapa_response = await query_kapa_api(input.message)
    if kapa_response:
        escaped_response = escape_markdown(kapa_response["answer"])
        return escaped_response
    else:
        return "Sorry, I couldn't fetch a response."


@activity.defn
async def query_kapa_api(query: str) -> Optional[dict]:
    url = f"{KAPA_API_ENDPOINT}//query/v1?query={query}"
    headers = {"X-API-TOKEN": KAPA_API_TOKEN}
    activity.heartbeat("Querying KAPA API")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                return data
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return None
