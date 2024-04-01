import os
import discord
import asyncio
import random
from dotenv import load_dotenv

from bday_bot.sentiment import analyze_sentiment
from bday_bot.data import (
    FACTS_AND_POLLS,
    KIND_SHELBY_REPLY,
    REPLY_TO_POSITIVE_RESPONSE,
    REPLY_TO_NEGATIVE_RESPONSE,
    REPLY_TO_NEUTRAL_RESPONSE,
    PATRONIZING_RESPONSE,
    REACTION_RESPONSES,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

BOT_CHANNEL = "shelby-bday-react-zone"

intents = discord.Intents.none()
intents.messages = True
intents.reactions = True


client = discord.Client(intents=intents)

# TARGET_SERVER = ("Queers for Fears", 1216970775052025876)
TARGET_SERVER = ("casey's server", 704379622627999744)


async def post_fun_fact_or_poll():
    # find the guild matching the target server
    guild = next(
        (guild for guild in client.guilds if guild.id == TARGET_SERVER[1]),
        None,
    )

    if not guild:
        print(f"Could not find server {TARGET_SERVER}")
        return

    channels = await guild.fetch_channels()
    channel = next(
        (
            channel
            for channel in channels
            if channel.name == BOT_CHANNEL and channel.type == discord.ChannelType.text
        ),
        None,
    )
    if not channel:
        channel = await guild.create_text_channel(
            BOT_CHANNEL, topic="Shelby is 30 today. Let's celebrate! 🎉"
        )

    await channel.send(
        "Hello - I am here to celebrate Shelby's birthday. Participation is mandatory."
    )
    await asyncio.sleep(2)
    await channel.send(
        "Let's all take a moment to appreciate Shelby by sharing how we feel about him through emoji."
    )

    for item in FACTS_AND_POLLS:

        if item["type"] == "fact":
            message = await channel.send(f"FACT: {item['text']}")
        else:
            message = await channel.send(f"POLL: {item['question']}")
            for reaction in item["reactions"]:
                await message.add_reaction(reaction)

        # Wait for 1.25 hours before posting again
        await asyncio.sleep(75 * 60)

    await channel.send(
        "That's all for now. Thanks for participating! Hope you had a happy birthday Shelby! 🎉🎉🎉"
    )


@client.event
async def on_message(message: discord.Message):
    assert client.user

    if client.user.mentioned_in(message):
        if "shelby" in message.author.name:
            await message.reply(random.choice(KIND_SHELBY_REPLY))
        elif message.author != client.user:
            sentiment = analyze_sentiment(message.content)
            if sentiment == "Positive":
                await message.reply(random.choice(REPLY_TO_POSITIVE_RESPONSE))
            elif sentiment == "Negative":
                await message.reply(random.choice(REPLY_TO_NEGATIVE_RESPONSE))
            else:
                await message.reply(random.choice(REPLY_TO_NEUTRAL_RESPONSE))


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    print(f"{user} reacted with {reaction} to message {reaction.message}")

    if "shelby" in user.name:
        await reaction.message.reply(random.choice(PATRONIZING_RESPONSE))

    if reaction.me:
        return

    if random.choice([True, False]):
        await reaction.message.reply(random.choice(REACTION_RESPONSES))


@client.event
async def on_ready():
    print(f"Bot is ready. Logged in as {client.user}")
    client.loop.create_task(post_fun_fact_or_poll())


def main():
    client.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
