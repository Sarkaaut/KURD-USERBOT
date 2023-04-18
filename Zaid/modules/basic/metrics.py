import time

from pyrogram import filters, Client
from pyrogram.types import Message

from Zaid.modules.help import add_command_help


class Custom(dict):
    def __missing__(self, key):
        return 0


@Client.on_message(filters.command("ژمارەی وشەکان", ".") & filters.me)
async def word_count(bot: Client, message: Message):
    await message.delete()
    words = Custom()
    progress = await bot.send_message(message.chat.id, "** 0 پەیامی پرۆسێس کراوە**")
    total = 0
    async for msg in bot.iter_history(message.chat.id, 1000):
        total += 1
        if total % 100 == 0:
            await progress.edit_text(f"پرۆسێس کراوە{total} پەیامەکان...")
            time.sleep(0.5)
        if msg.text:
            for word in msg.text.split():
                words[word.lower()] += 1
        if msg.caption:
            for word in msg.caption.split():
                words[word.lower()] += 1
    freq = sorted(words, key=words.get, reverse=True)
    out = "Word Counter\n"
    for i in range(25):
        out += f"{i + 1}. **{words[freq[i]]}**: {freq[i]}\n"

    await progress.edit_text(out)


add_command_help(
    "وشەکان",
    [
        [
            "ژمارەی وشەکان",
            "25 وشەی زۆرترین بەکارهێنراو لە دوایین 1000 نامە لە چاتی گروپ یان تایبەتدا دەدۆزێتەوە. بەکارهێنان لە"
            "چاتێک کە دەتەوێت پێوەرەکە تێیدا بدۆزیتەوە.",
        ],
    ],
)
