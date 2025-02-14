from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message


from Zaid.modules.help import add_command_help

spam_chats = []


def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

@Client.on_message(filters.command("تاگ", ".") & filters.me)
async def mentionall(client: Client, message: Message):
    chat_id = message.chat.id
    direp = message.reply_to_message
    args = get_arg(message)
    if not direp and not args:
        return await message.edit("**نامەیەکم بۆ بنێرە یان وەڵامی نامەیەک بدەرەوە!**")
    await message.delete()
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}), "
        if usrnum == 5:
            if args:
                txt = f"{args}\n\n{usrtxt}"
                await client.send_message(chat_id, txt)
            elif direp:
                await direp.reply(usrtxt)
            await sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@Client.on_message(filters.command("وە ستان", ".") & filters.me)
async def cancel_spam(client: Client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.edit("**پێدەچێت لێرەدا هیچ تاگی نەبێت**")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.edit("**هەڵوەشایەوە**")


add_command_help(
    "تاگ",
    [
        [
            "تاگ",
            "یەک بە یەک هەموو ئەندامەکان تاگ بکەن",
        ],
        [
            "وە ستان",
            f"بۆ وەستاندنی تاگ تە نها فە رمانە کە بنیرە",
        ],
    ],
)
