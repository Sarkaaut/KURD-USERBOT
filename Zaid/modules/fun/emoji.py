import asyncio
from collections import deque
from random import randint

from pyrogram import filters, Client
from pyrogram.types import Message


from Zaid.modules.help import add_command_help

emojis = {
    "مانگ": list("🌗🌘🌑🌒🌓🌔🌕🌖"),
    "کاتژمێر": list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"),
    "گەوارە": list("☀️🌤️⛅🌥️☁️🌩️🌧️⛈️⚡🌩️🌧️🌦️🌥️⛅🌤️☀️"),
    "زەوی": list("🌏🌍🌎🌎🌍🌏🌍🌎"),
    "دڵ": list("❤️🧡💛💚💙💜🖤"),
    "ماچ": list("🙈💋🙈💋🙈💋🙈"),
}
emoji_commands = [x for x in emojis]


@Client.on_message(filters.command(emoji_commands, ".") & filters.me)
async def emoji_cycle(bot: Client, message: Message):
    deq = deque(emojis[message.command[0]])
    try:
        for _ in range(randint(16, 32)):
            await asyncio.sleep(0.3)
            await message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except Exception:
        await message.delete()


special_emojis_dict = {
    "تیرک": {"emoji": "🎯", "help": "ئیمۆجی تایبەتی تیرک"},
    "دۆمینە": {"emoji": "🎲", "help": "ئیمۆجی تایبەتی دۆمینە"},
    "باسکە": {"emoji": "🏀", "help": "ئیمۆجی تایبەتی باسکە"},
    "تۆپی پێ": {"emoji": "⚽️", "help": "ئیمۆجی تایبەتی تۆپی پێ"},
}
special_emoji_commands = [x for x in special_emojis_dict]


@Client.on_message(filters.command(special_emoji_commands, ".") & filters.me)
async def special_emojis(bot: Client, message: Message):
    emoji = special_emojis_dict[message.command[0]]
    await message.delete()
    await bot.send_dice(message.chat.id, emoji["emoji"])


# Command help section
special_emoji_help = [
    ["مانگ", "هەموو قۆناغەکانی ئیمۆجیەکانی مانگ دەسوڕێتەوە"],
    ["کاتژمێر", "هەموو قۆناغەکانی ئیمۆجی کاتژمێرەکان دەسوڕێنێت"],
    ["گەوارە", "هه وره كان ڕەشەبا دەکەن"],
    ["دڵ", "ئیمۆجی دڵی خول دەکات"],
    ["زەوی", "جیهان وا لێبکە بە دەوری خۆیدا بڕوات"],
]

for x in special_emojis_dict:
    special_emoji_help.append([f".{x}", special_emojis_dict[x]["help"]])

add_command_help("ئیمۆجی", special_emoji_help)
