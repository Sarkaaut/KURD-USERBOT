import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import Message
from requests import get


from Zaid import SUDO_USER

from Zaid.modules.help import add_command_help
from cache.data import GROUP, VERIFIED_USERS
NB = GROUP
DEVS = VERIFIED_USERS

def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

@Client.on_message(
    filters.command(["فوروارد"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def gcast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        tex = await message.reply_text("دەستی بە فوروارد کرد...")
    else:
        return await message.edit_text("**پەیامێک یان وەڵامێک بدەرەوە**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in NB:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await tex.edit_text(
        f"**بە سەرکەوتوویی نامە بۆ** `{done}` **گروپەکان، چاتەکان، شکستی هێنا لە ناردنی نامە بۆ** `{error}` **گروپەکان**"
    )


@Client.on_message(
    filters.command(["فوروارد گروپ"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def gucast(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        tex = await message.reply_text("دەستی بە فوروارد کرد...")
    else:
        return await message.edit_text("** پەیامێک یان وەڵامێک بدەرەوە**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in DEVS:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await text.edit_text(
        f"** بە سەرکەوتوویی نامە بۆ** {done} ** چات شکستی هێنا لە ناردنی نامە بۆ** `{error}` ** چات**"
    )


add_command_help(
    "فوروارد",
    [
        [
            "فوروارد",
            "ناردنی پەیامی پەخشی جیهانی بۆ هەموو ئەو گروپانەی کە چوویتە ناویەوە. (دەتوانێت میدیا ستیکەر بنێرێت)",
        ],
        [
            "فوروارد گروپ",
            "ناردنی پەیامی پەخشی جیهانی بۆ هەموو مەساجەکانی تایبەت  کۆمپیوتەرەکانی داهاتوو. (دەتوانێت میدیا ستیکەر بنێرێت)",
        ],
    ],
)
