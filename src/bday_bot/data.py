POLLS = [
    # {
    #     "id": "pizza-poll",
    #     "type": "poll",
    #     "question": "What is Shelby's favorite pizza topping?",
    #     "reactions": ["🍕", "🍍", "🍖", "🍅", "🍆"],
    # },
    {
        "id": "animal-poll",
        "type": "poll",
        "question": "Which zoo animal is Shelby's favorite?",
        "reactions": ["🐘", "🐶", "🐧", "👶"],
    },
    {
        "id": "ice-cream-poll",
        "type": "poll",
        "question": "If Shelby could eat ice cream, what flavor would they choose?",
        "reactions": ["🍦", "🍨", "🦁"],
    },
    {
        "id": "fmk-poll",
        "type": "poll",
        "question": "FMK: Shelby, Shelbs, Dr. S",
        "reactions": ["🔥", "💔", "👻"],
    },
    {
        "id": "literally-poll",
        "type": "poll",
        "question": "If Shelby won the lottery, what would he buy first?",
        "reactions": ["🌕", "🐒", "🏝️", "🍣"],
    },
]


# Each fact ends with an ironic emoji
FUN_FACTS = [
    "Shelby was born with a full set of teeth! 😬",
    "Shelby has killed and can't wait to kill again 😈",
    "Shelby once got runner up in a hotdog eating quiz! 🌭",
    "Shelby has a pet rock named Rocky, a pet stick named Sticky, and tupperware of unknown slime named Scooby Goo! 🐶",
    "Shelby has a secret talent for juggling the stresses of daily life! 🤹",
]

FUN_FACT_ITEMS = [
    {
        "id": f"fun-fact-{hash(fact)}",
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
    "That is so interesting",
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

NON_EXISTING_REACTION_RESPONSES = [
    "The options I gave you weren't good enough?",
    "You just had to pick something else, didn't you?",
    "Look at the beautiful options I gave you, and you chose something else",
]
