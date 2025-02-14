from random import randint
from typing import Optional

from pyrogram import Client, enums, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message
from Zaid import SUDO_USER
from pyrogram.types import Message
from Zaid.modules.help import add_command_help


def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.edit(f"** هیچ پەیوەندییەکی گروپی نەدۆزراوەتەوە** {err_msg}")
    return 


@Client.on_message(
    filters.command(["تيل"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def opengc(client: Client, message: Message):
    flags = " ".join(message.command[1:])
    tex = await message.reply_text(message, "پرۆسێسکردن. . .")
    vctitle = get_arg(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    args = f"** دەستی بە پەیوەندی گروپی کرد\n • ** ناسنامەی چات** : `{chat_id}`"
    try:
        if not vctitle:
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                )
            )
        else:
            args += f"\n • ** ناونیشان:** `{vctitle}`"
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                    title=vctitle,
                )
            )
        await tex.edit(args)
    except Exception as e:
        await tex.edit(f"** زانیاری:** `{e}`")


@Client.on_message(
    filters.command(["داخستن"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def end_vc_(client: Client, message: Message):
    chat_id = message.chat.id
    if not (
        group_call := (
            await get_group_call(client, message, err_msg=", پەیوەندی گروپی پیشتر کۆتایی هات")
        )
    ):
        return
    await client.invoke(DiscardGroupCall(call=group_call))
    await message.reply_text(f"کۆتایی هات بە پەیوەندی گروپی ** ناسنامەی چات** : `{chat_id}`")


add_command_help(
    "پەیوەندی",
    [
        ["تيل", "دەست بکە بە چاتی دەنگی گروپ"],
        ["داخستن", "کۆتایی هێنان بە چاتی دەنگی گروپ"],
    ],
)
