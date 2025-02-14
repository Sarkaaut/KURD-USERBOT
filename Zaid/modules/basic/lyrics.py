import asyncio

from pyrogram import filters, Client
from pyrogram.types import Message

from Zaid import SUDO_USER
from Zaid.modules.help import add_command_help


@Client.on_message(
    filters.command(["l", "تێکستەکان"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def send_lyrics(bot: Client, message: Message):
    try:
        cmd = message.command

        song_name = ""
        if len(cmd) > 1:
            song_name = " ".join(cmd[1:])
        elif message.reply_to_message:
            if message.reply_to_message.audio:
                song_name = f"{message.reply_to_message.audio.title} {message.reply_to_message.audio.performer}"
            elif len(cmd) == 1:
                song_name = message.reply_to_message.text
        elif not message.reply_to_message and len(cmd) == 1:
            await message.edit("ناوی گۆرانییەک بدە")
            await asyncio.sleep(2)
            await message.delete()
            return

        await message.edit(f"بەدەستهێنانی تێکستی گۆرانی بۆ`{song_name}`")
        lyrics_results = await bot.get_inline_bot_results("ilyricsbot", song_name)

        try:
            # send to Saved Messages because hide_via doesn't work sometimes
            saved = await bot.send_inline_bot_result(
                chat_id="من",
                query_id=lyrics_results.query_id,
                result_id=lyrics_results.results[0].id,
            )
            await asyncio.sleep(3)

            # forward from Saved Messages
            await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id="من",
                message_id=saved.updates[1].message.id,
            )

            # delete the message from Saved Messages
            await bot.delete_messages("من", saved.updates[1].message.id)
        except TimeoutError:
            await message.edit("ئەوەش سەری نەگرت")
            await asyncio.sleep(2)
        await message.delete()
    except Exception as e:
        await message.edit("شکستی هێنا لە دۆزینەوەی تێکستەکان")
        await asyncio.sleep(2)
        await message.delete()


add_command_help("تێکستەکان", [["تێکستەکان", "بەدوای تێکستەکاندا بگەڕێ و بنێرن"]])
