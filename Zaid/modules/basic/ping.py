import time
from datetime import datetime

import speedtest
from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from Zaid import StartTime, app, SUDO_USER
from Zaid.helper.PyroHelpers import SpeedConvert
from Zaid.modules.bot.inline import get_readable_time

from Zaid.modules.help import add_command_help

class WWW:
    SpeedTest = (
        "Speedtest started at `{start}`\n\n"
        "Ping:\n{ping} ms\n\n"
        "Download:\n{download}\n\n"
        "Upload:\n{upload}\n\n"
        "ISP:\n__{isp}__"
    )

    NearestDC = "Country: `{}`\n" "Nearest Datacenter: `{}`\n" "This Datacenter: `{}`"

@Client.on_message(
    filters.command(["خێرایی بۆت"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def speed_test(client: Client, message: Message):
    new_msg = await message.reply_text("تاقیکردنەوەی خێرایی بۆت . . .")
    try:
       await message.delete()
    except:
       pass
    spd = speedtest.Speedtest()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "بەدەستهێنانی باشترین سێرڤەر لەسەر بنەمای ping . . ."
    )
    spd.get_best_server()

    new_msg = await new_msg.edit(f"`{new_msg.text}`\n" "تاقیکردنەوەی خێرایی دابەزاندن . . .")
    spd.download()

    new_msg = await new_msg.edit(f"`{new_msg.text}`\n" "تاقیکردنەوەی خێرایی بارکردن . . .")
    spd.upload()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "بەدەستهێنانی ئەنجام و ئامادەکردنی فۆرماتکردن . . ."
    )
    results = spd.results.dict()

    await new_msg.edit(
        WWW.SpeedTest.format(
            start=results["مۆری کات"],
            ping=results["پینگ"],
            download=SpeedConvert(results["download"]),
            upload=SpeedConvert(results["upload"]),
            isp=results["کلایەنت"]["isp"],
        )
    )



@Client.on_message(
    filters.command(["پینگ"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def pingme(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    xx = await message.reply_text("**0% ▒▒▒▒▒▒▒▒▒▒**")
    try:
       await message.delete()
    except:
       pass
    await xx.edit("**20% ██▒▒▒▒▒▒▒▒**")
    await xx.edit("**40% ████▒▒▒▒▒▒**")
    await xx.edit("**60% ██████▒▒▒▒**")
    await xx.edit("**80% ████████▒▒**")
    await xx.edit("**100% ██████████**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await xx.edit(
        f"├• **╰☞Ping™╮**\n"
        f"├• **╰☞** - `%sms`\n"
        f"├• **╰☞ -** `{uptime}` \n"
        f"└• **╰☞:** {client.me.mention}" % (duration)
    )


add_command_help(
    "پینگ",
    [
        ["پینگ", "بۆت بە زیندووی بپشکنە"],
    ],
)
