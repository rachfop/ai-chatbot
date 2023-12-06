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
    url = f"{KAPA_API_ENDPOINT}//query/v1?query={input.message}"
    headers = {"X-API-TOKEN": KAPA_API_TOKEN}
    activity.heartbeat("Querying KAPA API")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and "answer" in data:
                        escaped_response = escape_markdown(data["answer"])
                        return escaped_response
                return "Sorry, I couldn't fetch a response."
    except RuntimeError as e:
        logging.error(f"RuntimeError occurred: {e}")
        return "Sorry, an error occurred while fetching the response."


@activity.defn
async def send_tweet_message(input: BotParams) -> str:
    activity.heartbeat("Sending tweet")
    # Here you would integrate with the Twitter API to send the actual tweet
    # For now, we just simulate it.
    return "Tweet sent"
