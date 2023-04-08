from asyncio import gather
from os import remove

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

from Zaid.helper.PyroHelpers import ReplyCheck
from Zaid.modules.basic.profile import extract_user

from Zaid.modules.help import add_command_help


@Client.on_message(filters.command(["zanyare", "زانیاری"], ".") & filters.me)
async def who_is(client: Client, message: Message):
    user_id = await extract_user(message)
    ex = await message.edit_text("پرۆسێسکردن. . .")
    if not user_id:
        return await ex.edit(
            "** ڕیپلە ی یان ئوزە ڕنیمی بە کارهێنە ڕ بکە بۆ وە ی زانیاری تە و ئەبین**"
        )
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("دۆخی بەکارهێنەر"):
            y = h.replace("دۆخی بەکارهێنەر", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""<b> زانیاری بەکارهێنەر:</b>

🆔 <b> ناونیشانی بەکارهێنەر:</b> <code>{user.id}</code>
👤 <b> ناوی یەکەم:</b> {first_name}
🗣️ <b> ناوی کۆتایی:</b> {last_name}
🌐 <b> ناوی بەکارهێنەر:</b> {username}
🏛️ <b> ئایدی:</b> <code>{dc_id}</code>
🤖 <b> بۆت:</b> <code>{user.is_bot}</code>
🚷 <b> سکام:</b> <code>{user.is_scam}</code>
🚫 <b> سنووردارە:</b> <code>{user.is_restricted}</code>
✅ <b> پشتڕاستکراوەتەوە:</b> <code>{user.is_verified}</code>
⭐ <b> نایاب:</b> <code>{user.is_premium}</code>
📝 <b> ژیاننامەی بەکارهێنەر:</b> {bio}

👀 <b> هەمان گروپەکان بینراون:</b> {len(common)}
👁️ <b> دوا بینین:</b> <code>{status}</code>
🔗 <b> بەستەری هەمیشەیی بەکارهێنەر:</b> <a href='tg://user?id={user.id}'>{fullname}</a>
"""
        photo_id = user.photo.big_file_id if user.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                ex.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=ReplyCheck(message),
                ),
            )
            remove(photo)
        else:
            await ex.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await ex.edit(f"** زانیاری:** `{e}`")


@Client.on_message(filters.command(["زانیاری گروپ", "zanyare chat", "زانیاری گروپ"], ".") & filters.me)
async def chatinfo_handler(client: Client, message: Message):
    ex = await message.edit_text("پرۆسێسکردن...")
    try:
        if len(message.command) > 1:
            chat_u = message.command[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await message.edit(
                    f"ئەم فرمانە لەناو گروپێکدا بەکاربهێنە یان زانیاری چات بەکاربهێنە"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("جۆری چات"):
            y = h.replace("جۆری چات", "")
            type = y.capitalize()
        else:
            type = "تایبەت"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""<b> زانیاری گروپ جات:</b>

🆔 <b> ناسنامەی چات:</b> <code>{chat.id}</code>
👥 <b> ناونیشان:</b> {chat.title}
👥 <b> ناوی بەکارهێنەر:</b> {username}
📩 <b> جۆر:</b> <code>{type}</code>
🏛️ <b> ئایدی:</b> <code>{dc_id}</code>
🗣️ <b> سکام:</b> <code>{chat.is_scam}</code>
🎭 <b> ساختەیە:</b> <code>{chat.is_fake}</code>
✅ <b> پشتڕاستکراوەتەوە:</b> <code>{chat.is_verified}</code>
🚫 <b> سنووردارە:</b> <code>{chat.is_restricted}</code>
🔰 <b> پارێزراوە:</b> <code>{chat.has_protected_content}</code>

🚻 <b> کۆی گشتی ئەندامان:</b> <code>{chat.members_count}</code>
📝 <b> وەسف:</b>
<code>{description}</code>
"""
        photo_id = chat.photo.big_file_id if chat.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                ex.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=ReplyCheck(message),
                ),
            )
            remove(photo)
        else:
            await ex.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await ex.edit(f"** زانیاری:** `{e}`")


add_command_help(
      "زانیاری",
    [
        [
            "زانیاری",
            "**زانیاری بەکارهێنەری تەلەگرام بەدەست بهێنە لەگەڵ وەسفێکی تەواو تە نها بە ریپلە ی**",
        ],
        [
            "زانیاری گروپ",
            "**زانیاری گروپ بەدەست بهێنە لەگەڵ وەسفێکی تەواو**",
        ],
    ],
)
