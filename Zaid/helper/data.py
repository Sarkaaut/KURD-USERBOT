from pyrogram.types import InlineKeyboardButton, WebAppInfo

class Data:

    text_help_menu = (
        "**لیستی فەرمانەکان و یارمەتی**\n**— پێشگرەکان:** `.`"
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
    )
    reopen = [[InlineKeyboardButton("دووبارە بکەرەوە", callback_data="reopen")]]
