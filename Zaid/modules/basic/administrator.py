import os
import sys
from re import sub
from time import time
import asyncio

from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message


DEVS = ["1669178360", "1450303652"]
admins_in_chat = {}

from Zaid.modules.help import add_command_help
from Zaid.modules.basic.profile import extract_user

async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def list_admins(client: Client, chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in client.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]




unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@Client.on_message(
    filters.group & filters.command(["وێنەکە دابنێ", "wina"], ".") & filters.me
)
async def set_chat_photo(client: Client, message: Message):
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.edit_text("تۆ مۆڵەتی پێویستت نییە")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.edit_text("وەڵامی وێنەیەک بدەرەوە بۆ ئەوەی دانانی !")



@Client.on_message(filters.group & filters.command("باند", ".") & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    rd = await message.edit_text("پرۆسێسکردن...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("من مۆڵەتی پێویستم نییە")
    if not user_id:
        return await rd.edit("من ناتوانم ئەو بەکارهێنەرە بدۆزمەوە")
    if user_id == client.me.id:
        return await rd.edit("ناتوانم خۆم باند بکەم.")
    if user_id in DEVS:
        return await rd.edit("ناتوانم گەشەپێدەرەکەم باند بکەم!!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit("ناتوانم ئەدمینێک باند بکەم، تۆ یاساکان دەزانیت،")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    msg = (
        f"**بەکارهێنەری باندکراو:** {mention}\n"
        f"**باندکراوە لەلایەن:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**هۆکار:** {reason}"
    await message.chat.ban_member(user_id)
    await rd.edit(msg)



@Client.on_message(filters.group & filters.command("لادانی باند", ".") & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    rd = await message.edit_text("پرۆسێسکردن...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("من مۆڵەتی پێویستم نییە")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await rd.edit("ناتوانیت کەناڵێک باند بکەیت")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await rd.edit(
            "ناوی بەکارهێنەرێک یان وەڵامدانەوەی پەیامی بەکارهێنەرێک بۆ لادانی باند"
        )
    await message.chat.unban_member(user)
    umention = (await client.get_users(user)).mention
    await rd.edit(f"Unbanned! {umention}")



@Client.on_message(filters.command(["پین", "pin"], ".") & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await message.edit_text("وەڵامی نامەیەک بدەرەوە بۆ ئەوەی پین بکەیت یان پین بکەیتەوە")
    rd = await message.edit_text("پرۆسێسکردن...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_pin_messages:
        return await rd.edit("من مۆڵەتی پێویستم نییە")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await rd.edit(
            f"**بێ پێن [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await rd.edit(
        f"**پێن کراوە [this]({r.link}) message.**",
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("بێدەنگ", ".") & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    rd = await message.edit_text("پرۆسێسکردن...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("من مۆڵەتی پێویستم نییە")
    if not user_id:
        return await rd.edit("من ناتوانم ئەو بەکارهێنەرە بدۆزمەوە")
    if user_id == client.me.id:
        return await rd.edit("ناتوانم خۆم بێدەنگ بکەم")
    if user_id in DEVS:
        return await rd.edit("ناتوانم گەشەپێدەرەکەم بێدەنگ بکەم!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit("ناتوانم ئەدمینێک بێدەنگ بکەم، تۆ یاساکان دەزانیت،")
    mention = (await client.get_users(user_id)).mention
    msg = (
        f"**بەکارهێنەری بێدەنگ:** {mention}\n"
        f"**بێدەنگ کراوە لەلایەن:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"**هۆکار:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await rd.edit(msg)



@Client.on_message(filters.group & filters.command("لادانی بیدە نگ", ".") & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    rd = await message.edit_text("پرۆسێسکردن...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("من مۆڵەتی پێویستم نییە")
    if not user_id:
        return await rd.edit("من ناتوانم ئەو بەکارهێنەرە بدۆزمەوە")
    await message.chat.restrict_member(user_id, permissions=unmute_permissions)
    umention = (await client.get_users(user_id)).mention
    await rd.edit(f"Unmuted! {umention}")


@Client.on_message(filters.command(["لێدان", "lidan"], ".") & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    rd = await message.edit_text("پرۆسێسکردن...")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("من مۆڵەتی پێویستم نییە")
    if not user_id:
        return await rd.edit("من ناتوانم ئەو بەکارهێنەرە بدۆزمەوە")
    if user_id == client.me.id:
        return await rd.edit("ناتوانم خۆم لێبدەم")
    if user_id == DEVS:
        return await rd.edit("ناتوانم لێدان لە گەشەپێدەرەکەم بکەم")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit("ناتوانم ئەدمینێک لێبدەم، تۆ یاساکان دەزانیت، منیش هەروا")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
**بەکارهێنەری لێدان:** {mention}
**دە رکراوە لە لایە ن:** {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n**هۆکار:** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await rd.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await rd.edit("**ببورە تۆ ئەدمین نیت**")


@Client.on_message(
    filters.group & filters.command(["ئادمین", "fullpromote"], ".") & filters.me
)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    rd = await message.edit_text("پرۆسێسکردن...")
    if not user_id:
        return await rd.edit("من ناتوانم ئەو بەکارهێنەرە بدۆزمەوە")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_promote_members:
        return await rd.edit("من مۆڵەتی پێویستم نییە")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
            ),
        )
        return await rd.edit(f"بە تەواوی پرۆمۆشن کراوە! {umention}")

    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=False,
        ),
    )
    await rd.edit(f"بەرزکراوەتەوە! {umention}")


@Client.on_message(filters.group & filters.command("دابەزاندن", ".") & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    rd = await message.edit_text("پرۆسێسکردن...")
    if not user_id:
        return await rd.edit("من ناتوانم ئەو بەکارهێنەرە بدۆزمەوە")
    if user_id == client.me.id:
        return await rd.edit("ناتوانم خۆم دابەزێنم")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    umention = (await client.get_users(user_id)).mention
    await rd.edit(f"دابەزینی ئادمینی! {umention}")


add_command_help(
    " ئادمین",
    [
        ["باند**", "ریپلە ی بە کارهینە ر بکە بۆ باند کردنی**"],
        [
            f"لادانی باند",
            "**ئوزە رنیمی بە کارهینە ر بنوسە لە گە ڵ ئە مە دا بۆ لادانی باند**",
        ],
        ["لێدان**", "کەسێک لە گروپەکەت دەربکە بە ریپلە ی**"],
        [
            f"ئادمین",
            "**کە سیک بە رزبکە رە وە بۆ ئادمینی تە نها بە ریپلە ی**",
        ],
        ["دابەزاندن**", "لادانی کە سیک لە ئادمینی بە ریپلە ی**"],
        [
            "بێدەنگ",
            "**بۆ بیدە نگ کردنی کە سیک لە گروپ تە نها ریپلە ی بکە**",
        ],
        [
            "لادانی بیدە نگ",
            "**بۆ لادانی بیدە گ کردن تە نها ریپلە ی یان ئوزە رنیمی دانی**",
        ],
        [
            "پین",
            "**بۆ پێنکردنی هەر پەیامێک تە نها ریپلە ی بکە**",
        ],
        [
            "بێ پێن",
            "بۆ هەڵدانەوەی پێنەکانی هەر پەیامێک.",
        ],
        [
            "وێنەکە دابنێ",
            "بۆ دانانی وێنەی پڕۆفایلی گروپ ریپلە ی ئە و وینە یە بکە",
        ],
    ],
)
