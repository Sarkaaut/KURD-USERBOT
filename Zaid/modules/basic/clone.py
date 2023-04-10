import os

from pyrogram import *
from pyrogram.types import *


from Zaid.helper.basic import edit_or_reply, get_text, get_user

from Zaid.modules.help import *

OWNER = os.environ.get("OWNER", None)
BIO = os.environ.get("BIO", "404 : Bio Lost")


@Client.on_message(filters.command("کۆپیکردن", ".") & filters.me)
async def clone(client: Client, message: Message):
    text = get_text(message)
    op = await message.edit_text("کۆپی کردنی پروفایل")
    userk = get_user(message, text)[0]
    user_ = await client.get_users(userk)
    if not user_:
        await op.edit("پروفایلی کی کۆپی بکە م:(")
        return

    get_bio = await client.get_chat(user_.id)
    f_name = user_.first_name
    c_bio = get_bio.bio
    pic = user_.photo.big_file_id
    poto = await client.download_media(pic)

    await client.set_profile_photo(photo=poto)
    await client.update_profile(
        first_name=f_name,
        bio=c_bio,
    )
    await message.edit(f"**ئیستا پروفایلم هاوشیوە ی پروفایلی ئەو کە سە یە** __{f_name}__")


@Client.on_message(filters.command("گەڕانەوە", ".") & filters.me)
async def revert(client: Client, message: Message):
    await message.edit("گەڕانەوە بۆ پروفایلی پیشتر")
    r_bio = BIO

    # Get ur Name back
    await client.update_profile(
        first_name=OWNER,
        bio=r_bio,
    )
    # Delte first photo to get ur identify
    photos = [p async for p in client.get_chat_photos("من")]
    await client.delete_profile_photos(photos[0].file_id)
    await message.edit("ئیستا پروفایلت وە ک جارانی لی هاتووە!")


add_command_help(
    "کۆپی",
    [
        ["کۆپیکردن**", "بۆ کۆپی کردنی پرۆفایلی کەسێک**"],
        ["گەڕانەوە**", "بۆ ئەوەی ئەکاونتەکەت بگەڕێتەوە سە ر پروفایلی پیشتر**"],
    ],
)
