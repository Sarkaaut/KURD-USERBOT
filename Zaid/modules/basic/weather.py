import asyncio
from html import escape

import aiohttp
from pyrogram import filters, Client 
from pyrogram.types import Message

from Zaid.modules.help import add_command_help
from pyrogram import enums

@Client.on_message(filters.command(["کەشوهەوا", "kashohawa"], ".") & filters.me)
async def get_weather(bot: Client, message: Message):
    if len(message.command) == 1:
        await message.edit("بەکارهێنان: `. کەشوهەوا iraq `")
        await asyncio.sleep(3)
        await message.delete()

    if len(message.command) > 1:
        location = message.command[1]
        headers = {"user-agent": "httpie"}
        url = f"https://wttr.in/{location}?mnTC0&lang=en"
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as resp:
                    data = await resp.text()
        except Exception:
            await message.edit("نەیتوانی پێشبینی کەشوهەوا بەدەست بهێنێت")

        if "ئەمڕۆ زیاتر لە 1M داواکاریمان پرۆسێس کرد" in data:
            await message.edit("ببورن ئەمڕۆ ناتوانین ئەم داواکارییە پرۆسێس بکەین!")
        else:
            weather = f"<code>{escape(data.replace('ڕاپۆرت', 'ڕاپۆرت'))}</code>"
            await message.edit(weather, parse_mode=enums.ParseMode.MARKDOWN)


add_command_help(
    " کەشوهەوا",
    [
        ["کەشوهەوا**", "زانیاری کەشوهەوا بۆ شوێنی دابینکراو وەردەگرێت**"],
    ],
)
