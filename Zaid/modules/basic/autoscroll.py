from pyrogram import filters, Client
from pyrogram.types import Message

from Zaid.modules.help import add_command_help

the_regex = r"^r\/([^\s\/])+"

f = filters.chat([])

if f:
   @Client.on_message(f)
   async def auto_read(bot: Client, message: Message):
       await bot.read_history(message.chat.id)
       message.continue_propagation()


@Client.on_message(filters.command("جوڵانی ئۆتۆماتیکی", ".") & filters.me)
async def add_to_auto_read(bot: Client, message: Message):
    if message.chat.id in f:
        f.remove(message.chat.id)
        await message.edit("ئۆتۆسکڕۆڵ ناچالاک کرا")
    else:
        f.add(message.chat.id)
        await message.edit("ئۆتۆسکڕۆڵ چالاک کراوە")


add_command_help(
    "جوڵانی ئۆتۆماتیکی",
    [
        [
            "جوڵانی ئۆتۆماتیکی",
            "لە هەر چاتێکدا autoscroll بنێرە بۆ ئەوەی بە شێوەیەکی ئۆتۆماتیکی هەموو نامە نێردراوەکان بخوێنیتەوە تا پەیوەندی دەکەیت"
            "جارێکی تر ئۆتۆسکڕۆڵ بکە. ئەمەش بەسوودە ئەگەر تێلێگرامت لەسەر شاشەیەکی تر کراوە بێت",
        ],
    ],
)
