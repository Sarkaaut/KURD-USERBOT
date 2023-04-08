from asyncio import sleep

from pyrogram import filters, Client 


from Zaid.helper.aiohttp_helper import AioHttp
from Zaid.modules.help import add_command_help


def replace_text(text):
    return text.replace('"', "").replace("\\r", "").replace("\\n", "").replace("\\", "")


@Client.on_message(filters.me & filters.command(["پێناسە"], "."))
async def urban_dictionary(bot, message):
    if len(message.text.split()) == 1:
        await message.edit("بەکارهێنان: ud نموونە")
        return
    try:
        text = message.text.split(None, 1)[1]
        response = await AioHttp().get_json(
            f"http://api.urbandictionary.com/v0/define?term={text}"
        )
        word = response["لیست"][0]["ووشە"]
        definition = response["لیست"][0]["پێناسە"]
        example = response["لیست"][0]["نموونە"]
        resp = (
            f"** دەق: {replace_text(word)}**\n"
            f"** واتا:**\n`{replace_text(definition)}`\n\n"
            f"** نموونە:**\n`{replace_text(example)}` "
        )
        await message.edit(resp)
        return
    except Exception as e:
        await message.edit("نەتوانرا دەست بە API ی فەرهەنگی شارەکان بگات")
        print(e)
        await sleep(3)
        await message.delete()



add_command_help(
    "پێناسە",
    [
        ["پێناسە**", "پێناسەی ئەو وشەیە بکە کە دەینێری یان وەڵامی دەدەیتەوە**"],
    ],
)
