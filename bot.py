print("🚀 Starting bot...")

# This import triggers model loading
import models

import discord
from rag_pipeline import chat_model

from config import (
    BOT_TOKEN
)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("🤖 Bot is online and ready!")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)

    response = await chat_model(user_id, message.content)
    await message.channel.send(response)


client.run(BOT_TOKEN)
