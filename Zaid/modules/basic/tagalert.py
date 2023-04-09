from pyrogram import Client, enums, filters 
from pyrogram.types import Message 
from config import LOG_GROUP
from Zaid.modules.help import add_command_help
log = []


@Client.on_message(filters.command("چالاککردن", ".") & filters.me)
async def set_no_log_p_m(client: Client, message: Message):
    if LOG_GROUP != -100:
        if not message.chat.id in log:
            log.append(message.chat.id)
            await message.edit("**ئاگادارکردنەوەی تاگ بە سەرکەوتوویی چالاک کرا**")

@Client.on_message(filters.command("ناچالاککردن", ".") & filters.me)
async def set_no_log_p_m(client: Client, message: Message):
        if not message.chat.id in log:
            log.remove(message.chat.id)
            await message.edit("**ئاگادارکردنەوەی تاگ بە سەرکەوتوویی چالاک نەکراوە**")

if log:
 @Client.on_message(filters.group & filters.mentioned & filters.incoming)
 async def log_tagged_messages(client: Client, message: Message):
    result = f"<b>📨 #TAGS #MESSAGE</b>\n<b> • : </b>{message.from_user.mention}"
    result += f"\n<b> • Group : </b>{message.chat.title}"
    result += f"\n<b> • 👀 </b><a href = '{message.link}'>Lihat Pesan</a>"
    result += f"\n<b> • Message : </b><code>{message.text}</code>"
    await asyncio.sleep(0.5)
    await client.send_message(
        LOG_GROUP,
        result,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )


add_command_help(
    "ئاگادارکردنه وه",
    [
        [
            "چالاککردن",
            "**بۆ چالاککردن تاگی گروپ، کە دەچێتە سەر گروپی لۆگ**",
            "ناچالاککردن",
            "بۆ ناچالاککردن تاگی گروپ، کە دەچێتە سەر گروپی لۆگ",

        ],
    ],
)
