import asyncio
from functools import partial

from pyrogram import filters, Client 
from pyrogram.types import Message


from Zaid.modules.help import add_command_help

mention = partial("<a href='tg://user?id={}'>{}</a>".format)

hmention = partial("<a href='tg://user?id={}'>\u200B</a>{}".format)


@Client.on_message(filters.command("ئاماژە پێکردن", ".") & filters.me)
async def mention_user(bot: Client, message: Message):
    if len(message.command) < 3:
        await message.edit("فۆرماتێکی هەڵە\nنموونە: . ئاماژە پێکردن @Sarkaut سڵاو")
        await asyncio.sleep(3)
        await message.delete()
        return
    try:
        user = await bot.get_users(message.command[1])
    except Exception:
        await message.edit("بەکارهێنەر نەدۆزرایەوە")
        await asyncio.sleep(3)
        await message.delete()
        return

    _mention = mention(user.id, " ".join(message.command[2:]))
    await message.edit(_mention)


@Client.on_message(filters.command("ئاماژە ی شاراوە", ".") & filters.me)
async def hidden_mention(bot: Client, message: Message):
    if len(message.command) < 3:
        await message.edit("فۆرماتێکی هەڵە\nنموونە: . ئاماژە ی شاراوە @SARKAUT سڵاو")
        await asyncio.sleep(3)
        await message.delete()
        return
    try:
        user = await bot.get_users(message.command[1])
    except Exception:
        await message.edit("بەکارهێنەر نەدۆزرایەوە")
        await asyncio.sleep(3)
        await message.delete()
        return

    _hmention = hmention(user.id, " ".join(message.command[2:]))
    await message.edit(_hmention)



add_command_help(
    "ئاماژە پێکردن",
    [
        [
            "ئاماژە پێکردن",
            "ئاماژە بە بەکارهێنەرێک بکە بە ناوێکی جیاواز\nنموونە: ئاماژە پێکردن @user سڵاو",
        ],
        [
            "ئاماژە ی شاراوە",
            "باسی بەکارهێنەرێک بکە کە دەقێکی شاراوەی هەبێت\نموونە: . ئاماژە پێکردن @user",
        ],
    ],
)
