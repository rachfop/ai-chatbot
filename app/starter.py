import logging
import os
from typing import Optional

from activities.activities import BotParams, send_tweet_message
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from temporalio.client import Client
from workflows.workflows import HandleStartCommand, HandleUserMessage

load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def get_client() -> Client:
    return await Client.connect("localhost:7233")


# Function to handle /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    client = await get_client()
    chat_id = update.effective_chat.id
    bot_params = BotParams(message="", chat_id=chat_id)
    result = await client.execute_workflow(
        HandleStartCommand.run,
        bot_params,
        id=f"start-command-{chat_id}",
        task_queue="my-task-queue",
    )
    await update.message.reply_text(result, parse_mode="MarkdownV2")


# Function to handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    client = await get_client()
    message = update.message.text
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        "Your ChatBot is thinking and your question has been received\. You will get a response in about 10 seconds\.",
        parse_mode="MarkdownV2",
    )
    bot_params = BotParams(message=message, chat_id=chat_id)
    result = await client.execute_workflow(
        HandleUserMessage.run,
        bot_params,
        id=f"user-message-{chat_id}",
        task_queue="my-task-queue",
    )

    await update.message.reply_text(result, parse_mode="MarkdownV2")


# Main function to run the bot
if __name__ == "__main__":
    try:
        # Create the Application and pass it your bot's token.
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
        )

        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except RuntimeError as e:
        logging.error(f"Runtime error: {e}")
