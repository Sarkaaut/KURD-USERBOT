import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from Zaid.helper.utility import get_arg

from Zaid.modules.help import add_command_help


@Client.on_message(filters.me & filters.command(["ق", "ستیکەرێک"], "."))
async def quotly(client: Client, message: Message):
    args = get_arg(message)
    if not message.reply_to_message and not args:
        return await message.edit("** تکایە وەڵامی نامە بدەرەوە**")
    bot = "QuotLyBot"
    if message.reply_to_message:
        await message.edit("دروستکردنی کۆت. . .")
        await client.unblock_user(bot)
        if args:
            await client.send_message(bot, f"/qcolor {args}")
            await asyncio.sleep(1)
        else:
            pass
        await message.reply_to_message.forward(bot)
        await asyncio.sleep(5)
        async for quotly in client.search_messages(bot, limit=1):
            if quotly:
                await message.delete()
                await message.reply_sticker(
                    sticker=quotly.sticker.file_id,
                    reply_to_message_id=message.reply_to_message.id
                    if message.reply_to_message
                    else None,
                )
            else:
                return await message.edit("** شکستی هێنا لە دروستکردنی ستیکەری Quotly**")


add_command_help(
    "ستیکەرێک",
    [
        [
            f"ستیکەرێک",
            "**بۆ ئەوەی کۆتێک دروست بکەیت**",
        ],
        [
            f"يان ته نها پيتي (ق) بنوسه",
            "**پەیامێک بکە بە ستیکەرێک بە ڕەنگی پاشبنەمای تایبەت کە پێی دراوە**",
        ],
    ],
)
