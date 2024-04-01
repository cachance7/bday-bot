import os
import discord
import asyncio
import random
from dotenv import load_dotenv

from bday_bot.sentiment import analyze_sentiment

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

BOT_CHANNEL = "shelby-bday-react-zone"

intents = discord.Intents.none()
intents.messages = True
intents.reactions = True

POLLS = [
    {
        "type": "poll",
        "question": "What is Shelby's favorite pizza topping?",
        "reactions": ["🍕", "🍍", "🍖", "🍄", "🍅"],
    },
    {
        "type": "poll",
        "question": "Which zoo animal is Shelby's least favorite?",
        "reactions": ["🦁", "🐘", "🐶", "🐧", "👶"],
    },
    {
        "type": "poll",
        "question": "If Shelby could eat ice cream, what flavor would they choose?",
        "reactions": ["🍦", "🍨", "🍧", "🍭"],
    },
    {
        "type": "poll",
        "question": "FMK: Shelby, Shelbs, Dr. S",
        "reactions": ["🔥", "💔", "👻"],
    },
    {
        "type": "poll",
        "question": "Can Shelby literally not even?",
        "reactions": ["🙅", "🌕", "🙇", "🙈", "👽"],
    },
]


# Each fact ends with an ironic emoji
FUN_FACTS = [
    "Shelby was born with a full set of teeth! 😬",
    "Shelby has killed and can't wait to kill again 😈",
    "Shelby once got runner up in a hotdog eating quiz! 🌭",
    "Shelby has a pet rock named Rocky, a pet stick named Sticky, and a bowl of unknown slime named Scooby Goo! 🐶",
    "Shelby has a secret talent for juggling the stresses of daily life! 🤹",
]

FUN_FACT_ITEMS = [
    {
        "type": "fact",
        "text": fact,
    }
    for fact in FUN_FACTS
]

FACTS_AND_POLLS = [*sum(zip(POLLS, FUN_FACT_ITEMS), ())]

KIND_SHELBY_REPLY = [
    "Happy birthday Shelby!",
    "Hello Shelby! You're looking great today, I'm sure!",
    "Hey Shelby! You're doing a great job!",
    "Hi Shelby! You're the best!",
    "Hello Shelby! You're amazing!",
]

PATRONIZING_RESPONSE = [
    "Shelby, it's nice that you reacted, but this poll isn't about what you think. It's about what everyone else thinks."
    "Shelby, I know you're excited, but now is not the time to share your opinion."
    "Shelby, I appreciate your enthusiasm, but let's let others have a chance to share their thoughts."
    "Shelby, I'm glad you're participating, but let's give others a chance to react too."
    "Shelby, I know you're eager to share your thoughts, but let's give others a chance to react first."
]

REPLY_TO_POSITIVE_RESPONSE = [
    "That's great to hear!",
    "I'm so happy for you!",
    "I'm glad you're having a good day!",
    "That's awesome!",
]

REPLY_TO_NEGATIVE_RESPONSE = [
    "That's just what you think.",
    "Why would you say that?",
    "I'm sorry?",
    "Cool I guess...",
]

REPLY_TO_NEUTRAL_RESPONSE = [
    "Gotcha",
    "Uhh...",
    "Hmm...",
    "Yeah I guess",
]

REACTION_RESPONSES = [
    "Wow, I'll bet Shelby would love to hear you said that",
    "And I thought Shelby was your friend",
    "I can't believe you would say that",
    "Shelby is going to be so mad at you",
    "I'm sure Shelby would disagree with you",
]

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

        # Wait for 2 minutes before posting again
        await asyncio.sleep(30)

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
