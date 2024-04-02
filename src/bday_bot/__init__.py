import os
import discord
import asyncio
import random
from dotenv import load_dotenv

from bday_bot.sentiment import analyze_sentiment
from bday_bot.data import (
    FACTS_AND_POLLS,
    FUN_FACT_ITEMS,
    KIND_SHELBY_REPLY,
    NON_EXISTING_REACTION_RESPONSES,
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

TARGET_SERVER = ("Queers for Fears", 1216970775052025876)
# TARGET_SERVER = ("casey's server", 704379622627999744)

item_lookup = {}


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
            BOT_CHANNEL, topic="Shelby is 30 today. Let's celebrate them! 🎉"
        )

    #
    # await channel.send(
    #     "Hello - I am here to celebrate Shelby's birthday. Participation is mandatory. @everyone"
    # )
    # await asyncio.sleep(2)
    # await channel.send(
    #     "Let's all take a moment to appreciate Shelby by sharing how we feel about him through emoji."
    # )

    for item in FUN_FACT_ITEMS:
        try:
            print(f"Posting item {item}")
            # await asyncio.sleep(5 * 60)

            if item["type"] == "fact":
                print(f"Posting fact {item['text']}")
                message = await channel.send(f"FACT: {item['text']}")
                item_lookup[message.id] = item
            else:
                print(f"Posting poll {item['question']}")
                message = await channel.send(f"POLL: {item['question']}")
                item_lookup[message.id] = item
                for reaction in item["reactions"]:
                    await message.add_reaction(reaction)
        except Exception as e:
            print(f"Error posting item {item}: {e}")

    print("All items posted. Waiting for 10 minutes before closing the channel.")
    await asyncio.sleep(10 * 60)

    try:
        # find lauren in the guild
        lauren = next(
            (
                member
                for member in guild.members
                if member.display_name.lower() == "lauren"
            ),
            None,
        )

        if lauren:
            await channel.send(f"Hey {lauren.mention}, nice answers! 🌟")

        # find al in the guild
        al = next(
            (member for member in guild.members if member.display_name == "al"), None
        )

        if al:
            await channel.send(f"Hey {al.mention}, fight me! 🤺")

        # find fisaurus
        fisaurus = next(
            (member for member in guild.members if member.display_name == "fisaurus"),
            None,
        )

        if fisaurus:
            await channel.send(f"Hey {fisaurus.mention}, I won our debate. 🏆")

        # find thurgen
        thurgen = next(
            (member for member in guild.members if member.display_name == "thurgen"),
            None,
        )

        if thurgen:
            await channel.send(f"Hey {thurgen.mention}, I saw you! 👀")

        # find shelby
        shelby = next(
            (member for member in guild.members if member.display_name == "shelby"),
            None,
        )

        if shelby:
            await channel.send(
                f"That's all for now. Thanks for participating! Some of you were great sports. Hope you had a happy birthday, {shelby.mention}! 🎉🎉🎉"
            )
            await channel.send(
                "https://www.canva.com/design/DAGBO9fkpyc/fokk6CElnMvoLQ1ILeNGog/view"
            )
    except Exception as e:
        await channel.send(
            f"That's all for now. Thanks for participating! Some of you were great sports. Hope you had a happy birthday, Shelby! 🎉🎉🎉"
        )
        await channel.send(
            "https://www.canva.com/design/DAGBO9fkpyc/fokk6CElnMvoLQ1ILeNGog/view"
        )


@client.event
async def on_message(message: discord.Message):
    assert client.user

    if not client.user.mentioned_in(message):
        return

    if (
        "shelby" == message.author.display_name
        or "btier" == message.author.display_name
    ):
        await message.reply(random.choice(KIND_SHELBY_REPLY))
        return

    if "al" == message.author.display_name:
        await message.reply(
            random.choice(["What were you told about antagonizing me?", "Fight me!"])
        )
        return

    if "fisaurus" == message.author.display_name:
        await message.reply(
            "I'm sorry, I can't hear you over the sound of how right I am.",
        )
        return

    if "thanks" in message.content.lower() or "thank you" in message.content.lower():
        await message.reply("No, thank YOU!")
        return

    if message.author != client.user:
        print(f"Received message: {message.content}")
        if "sing" in message.content:
            await message.reply(
                "🎶 Happy birthday to you! 🎶 Happy birthday to you! 🎶 Happy birthday dear Shelby! 🎶 Happy birthday to you! 🎶"
            )
            return

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

    item = item_lookup.get(reaction.message.id)
    if not item:
        print(f"Could not find item for message {reaction.message.id}")
        print(item_lookup)
        return

    if item["type"] != "poll":
        return

    if "shelby" == user.display_name or "btier" == user.display_name:
        await reaction.message.reply(random.choice(PATRONIZING_RESPONSE))
        return

    if user == client.user:
        return

    if item and reaction.emoji not in item["reactions"]:
        await reaction.message.reply(
            f"Really {user.mention}? {reaction.emoji}?"
            + " "
            + random.choice(NON_EXISTING_REACTION_RESPONSES)
        )
        return

    # if random.choice([True, False]):
    #     await reaction.message.reply(random.choice(REACTION_RESPONSES))
    #     return


@client.event
async def on_ready():
    print(f"Bot is ready. Logged in as {client.user}")
    client.loop.create_task(post_fun_fact_or_poll())


def main():
    client.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
