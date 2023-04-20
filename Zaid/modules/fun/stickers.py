import asyncio
import random

from pyrogram import filters, Client
from pyrogram.types import Message

from Zaid.helper.PyroHelpers import ReplyCheck
from Zaid.modules.help import add_command_help

sticker_data = {
    "گاڵتە پێکردن": {
        "value": 7,
        "empty_message": "شتێکم پێ بدە تا گاڵتە بکەم",
        "action": "گاڵتەکردن...",
    },
    "گەڕان": {
        "value": 12,
        "empty_message": "سێنپای، پێویستم بە شتێکە بۆ گووگڵ...",
        "action": "گووگڵکردن...",
    },
    "کچێکی ئەنیمێ": {
        "alts": ["ag", "کچێکی ئەنیمێ"],
        "value": [15, 20, 32, 33, 34, 40, 41, 42, 58],
        "empty_message": "وایفوەکە ڕایکرد...",
        "action": "داواکردن لە ویافوسەکەم کە بیڵێت...",
    },
    "ئەنیمێ کوڕیک": {
        "alts": ["ئەنیمێ کوڕیک"],
        "value": [37, 38, 48, 55],
        "empty_message": "سێنپای، پێویستم بە شتێکە بیڵێم...",
        "action": "کوڕەکان لەسەری بوون...",
    },
}

sticker_commands = []
for x in sticker_data:
    sticker_commands.append(x)
    if "alts" in sticker_data[x]:
        for y in sticker_data[x]["alts"]:
            sticker_commands.append(y)


@Client.on_message(filters.command(sticker_commands, ".") & filters.me)
async def sticker_super_func(bot: Client, message: Message):
    try:
        sticker = {}
        command = message.command[0]
        if command not in sticker_data:
            for sticker in sticker_data:
                if (
                        "alts" in sticker_data[sticker]
                        and command in sticker_data[sticker]["alts"]
                ):
                    sticker = sticker_data[sticker]
                    break
        else:
            sticker = sticker_data[message.command[0]]

        cmd = message.command

        sticker_text = ""
        if len(cmd) > 1:
            sticker_text = " ".join(cmd[1:])
        elif message.reply_to_message and len(cmd) == 1:
            sticker_text = message.reply_to_message.text
        elif not message.reply_to_message and len(cmd) == 1:
            await message.edit(sticker["empty_message"])
            await asyncio.sleep(2)
            await message.delete()
            return

        await message.edit(f"`{sticker['action']}`")

        values = sticker["value"]
        choice = None
        if isinstance(values, list):
            choice = int(random.choice(values))
        elif isinstance(values, int):
            choice = values

        if choice:
            sticker_results = await bot.get_inline_bot_results(
                "stickerizerbot", f"#{choice}" + sticker_text
            )
        else:
            sticker_results = await bot.get_inline_bot_results(
                "stickerizerbot", sticker_text
            )

        try:
            await bot.send_inline_bot_result(
                chat_id=message.chat.id,
                query_id=sticker_results.query_id,
                result_id=sticker_results.results[0].id,
                reply_to_message_id=ReplyCheck(message),
                hide_via=True,
            )
        except TimeoutError:
            await message.edit("@StickerizerBot لە کاتی خۆیدا وەڵامی نەدایەوە...")
            await asyncio.sleep(2)
    except Exception:
        await message.edit("نەیتوانی بگات @Stickerizerbot...")
        await asyncio.sleep(2)
    await message.delete()


add_command_help(
    "ستیکەریس",
    [
        [
            "گاڵتە پێکردن",
            "میمێکی گاڵتەجاڕی سپۆنجبۆب دەنێرێت کە چیت ناردووە بە فەرمان یان دەقی ئەوەی کە وەڵامت داوەتەوە\n"
        ],
        [
            "کچێکی ئەنیمێ",
            "ستیکەرێکی کچە ئەنیمێیەکی هەڕەمەکی دەنێرێت. یاساکان وەک لە سەرەوە جێبەجێ دەکرێن.",
        ],
        ["ئەنیمێ کوڕیک", "ستیکەرێکی کوڕی هەڕەمەکی دەنێرێت. یاساکان وەک لە سەرەوە جێبەجێ دەکرێن"],
        [
            "گەڕان",
            "دوگمەی گەڕانی گووگڵ دەنێرێت لەگەڵ ئەو پرسیارەی کە تۆ پێی دەدەیت. یاساکان وەک لە سەرەوە جێبەجێ دەکرێن.",
        ],
    ],
)
