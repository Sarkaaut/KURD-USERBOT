import asyncio

from pyrogram import filters, Client
from pyrogram.types import Message

from Zaid.helper.aiohttp_helper import AioHttp
from Zaid.modules.help import add_command_help


@Client.on_message(filters.command(["پێناسەکردن", "پ"], ".") & filters.me)
async def define(bot: Client, message: Message):
    cmd = message.command

    input_string = ""
    if len(cmd) > 1:
        input_string = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        input_string = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("**ناتوانێت تێپەڕێت بۆ بۆشایی**")
        await asyncio.sleep(2)
        await message.delete()
        return

    def combine(s_word, name):
        w_word = f"**__{name.title()}__**\n"
        for i in s_word:
            if "پێناسە" in i:
                if "نموونە" in i:
                    w_word += (
                            "\n**پێناسە**\n<pre>"
                            + i["پێناسە"]
                            + "</pre>\n<b>Example</b>\n<pre>"
                            + i["نموونە"]
                            + "</pre>"
                    )
                else:
                    w_word += (
                            "\n**پێناسە**\n" + "<pre>" + i["پێناسە"] + "</pre>"
                    )
        w_word += "\n\n"
        return w_word

    def out_print(word1):
        out = ""
        if "واتا" in list(word1):
            meaning = word1["واتا"]
            if "ناو" in list(meaning):
                noun = meaning["ناو"]
                out += combine(noun, "ناو")
            if "کردار" in list(meaning):
                verb = meaning["کردار"]
                out += combine(verb, "کردار")
            if "ئامازی پەیوەندی" in list(meaning):
                preposition = meaning["ئامازی پەیوەندی"]
                out += combine(preposition, "ئامازی پەیوەندی")
            if "هاوەڵکار" in list(meaning):
                adverb = meaning["هاوەڵکار"]
                out += combine(adverb, "هاوەڵکار")
            if "ئاوەڵناو" in list(meaning):
                adjec = meaning["ئاوەڵناو"]
                out += combine(adjec, ""ئاوەڵناو)
            if "کورتکراوەی" in list(meaning):
                abbr = meaning["کورتکراوەی"]
                out += combine(abbr, "کورتکراوەی")
            if "هاوارکردن" in list(meaning):
                exclamation = meaning["هاوارکردن"]
                out += combine(exclamation, "هاوارکردن")
            if "کرداری ڕاگوزەر" in list(meaning):
                transitive_verb = meaning["کرداری ڕاگوزەر"]
                out += combine(transitive_verb, "کرداری ڕاگوزەر")
            if "دیاریکەر" in list(meaning):
                determiner = meaning["دیاریکەر"]
                out += combine(determiner, "دیاریکەر")
                # print(determiner)
            if "crossReference" in list(meaning):
                crosref = meaning["crossReference"]
                out += combine(crosref, "crossReference")
        if "ناونیشان" in list(word1):
            out += (
                    "**تێبینی هەڵە**\n\n▪️`"
                    + word1["ناونیشان"]
                    + "\n\n▪️"
                    + word1["پەیام"]
                    + "\n\n▪️<i>"
                    + word1["بڕیار"]
                    + "</i>`"
            )
        return out

    if not input_string:
        await message.edit("وشە داخڵ بکە بۆ گەڕان تگایە ‼️")
    else:
        word = input_string
        r_dec = await AioHttp().get_json(
            f"https://api.dictionaryapi.dev/api/v1/entries/en/{word}"
        )

        v_word = input_string
        if isinstance(r_dec, list):
            r_dec = r_dec[0]
            v_word = r_dec["word"]
        last_output = out_print(r_dec)
        if last_output:
            await message.edit(
                "`Search result for   `" + f" {v_word}\n\n" + last_output
            )
        else:
            await message.edit("هیچ ئەنجامێک لە بنکەدراوە نەدۆزراوەتەوە")


add_command_help(
    "فەرهەنگ",
    [
        ["پێناسەکردن", "پێناسەی ئەو وشەیە بکە کە دەینێری یان وەڵامی دەدەیتەوە"],
    ],
)
