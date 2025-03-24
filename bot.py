import os
import threading
from traceback import format_exc

# Flask সংযুক্ত করা হচ্ছে
from flask import Flask
from telethon import Button, events

from core.bot import Bot
from core.executors import Executors
from database import DataBase
from functions.info import AnimeInfo
from functions.schedule import ScheduleTasks, Var
from functions.tools import Tools, asyncio
from functions.utils import AdminUtils
from libs.ariawarp import Torrent
from libs.logger import LOGS, Reporter
from libs.subsplease import SubsPlease

# Flask অ্যাপ তৈরি করা হচ্ছে
app = Flask(__name__)


@app.route("/health")
def health_check():
    return "Bot is running!", 200


def run_flask():
    # ডিফল্ট পোর্ট 5000, তবে পরিবেশ ভেরিয়েবল থেকে সেট করা যাবে
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)


tools = Tools()
tools.init_dir()
bot = Bot()
dB = DataBase()
subsplease = SubsPlease(dB)
torrent = Torrent()
schedule = ScheduleTasks(bot)
admin = AdminUtils(dB, bot)


@bot.on(
    events.NewMessage(
        incoming=True, pattern="^/start ?(.*)", func=lambda e: e.is_private
    )
)
async def _start(event):
    xnx = await event.reply("`Please Wait...`")
    msg_id = event.pattern_match.group(1)
    await dB.add_broadcast_user(event.sender_id)
    if Var.FORCESUB_CHANNEL and Var.FORCESUB_CHANNEL_LINK:
        is_user_joined = await bot.is_joined(Var.FORCESUB_CHANNEL, event.sender_id)
        if not is_user_joined:
            return await xnx.edit(
                "**Please Join The Following Channel To Use This Bot 🫡**",
                buttons=[
                    [Button.url("🚀 JOIN CHANNEL", url=Var.FORCESUB_CHANNEL_LINK)],
                    [
                        Button.url(
                            "♻️ REFRESH",
                            url=f"https://t.me/{(await bot.get_me()).username}?start={msg_id}",
                        )
                    ],
                ],
            )
    if msg_id:
        if msg_id.isdigit():
            msg = await bot.get_messages(Var.BACKUP_CHANNEL, ids=int(msg_id))
            await event.reply(msg)
        else:
            items = await dB.get_store_items(msg_id)
            if items:
                for id in items:
                    msg = await bot.get_messages(Var.CLOUD_CHANNEL, ids=id)
                    await event.reply(file=[i for i in msg])
    else:
        if event.sender_id == Var.OWNER:
            return await xnx.edit(
                "** <                ADMIN PANEL                 > **",
                buttons=admin.admin_panel(),
            )
        await event.reply(
            f"**Enjoy Ongoing Anime's Best Encode 24/7 🫡**",
            buttons=[
                [
                    Button.url("👨‍💻 DEV", url="t.me/RahatMx"),
                    Button.url("🕸️ Update Channel", url="https://t.me/AnimeTaboo"),
                ]
            ],
        )
    await xnx.delete()


@bot.on(
    events.NewMessage(incoming=True, pattern="^/about", func=lambda e: e.is_private)
)
async def _(e):
    await admin._about(e)


@bot.on(events.callbackquery.CallbackQuery(data="slog"))
async def _(e):
    await admin._logs(e)


@bot.on(events.callbackquery.CallbackQuery(data="sret"))
async def _(e):
    await admin._restart(e, schedule)


@bot.on(events.callbackquery.CallbackQuery(data="entg"))
async def _(e):
    await admin._encode_t(e)


@bot.on(events.callbackquery.CallbackQuery(data="butg"))
async def _(e):
    await admin._btn_t(e)


@bot.on(events.callbackquery.CallbackQuery(data="scul"))
async def _(e):
    await admin._sep_c_t(e)


@bot.on(events.callbackquery.CallbackQuery(data="cast"))
async def _(e):
    await admin.broadcast_bt(e)


@bot.on(events.callbackquery.CallbackQuery(data="bek"))
async def _(e):
    await e.edit(buttons=admin.admin_panel())


async def anime(data):
    try:
        torr = [data.get("480p"), data.get("720p"), data.get("1080p")]
        anime_info = AnimeInfo(torr[0].title)
        poster = await tools._poster(bot, anime_info)
        if await dB.is_separate_channel_upload():
            chat_info = await tools.get_chat_info(bot, anime_info, dB)
            await poster.edit(
                buttons=[
                    [
                        Button.url(
                            f"EPISODE {anime_info.data.get('episode_number', '')}".strip(),
                            url=chat_info["invite_link"],
                        )
                    ]
                ]
            )
            poster = await tools._poster(bot, anime_info, chat_info["chat_id"])
        btn = [[]]
        original_upload = await dB.is_original_upload()
        button_upload = await dB.is_button_upload()
        for i in torr:
            try:
                filename = f"downloads/{i.title}"
                reporter = Reporter(bot, i.title)
                await reporter.alert_new_file_founded()
                await torrent.download_magnet(i.link, "./downloads/")
                exe = Executors(
                    bot,
                    dB,
                    {
                        "original_upload": original_upload,
                        "button_upload": button_upload,
                    },
                    filename,
                    AnimeInfo(i.title),
                    reporter,
                )
                result, _btn = await exe.execute()
                if result:
                    if _btn:
                        if len(btn[0]) == 2:
                            btn.append([_btn])
                        else:
                            btn[0].append(_btn)
                        await poster.edit(buttons=btn)
                    asyncio.ensure_future(exe.further_work())
                    continue
                await reporter.report_error(_btn, log=True)
                await reporter.msg.delete()
            except BaseException:
                await reporter.report_error(str(format_exc()), log=True)
                await reporter.msg.delete()
    except BaseException:
        LOGS.error(str(format_exc()))


# Flask এবং টেলিগ্রাম বট একসাথে চালানোর জন্য থ্রেড ব্যবহার করা হচ্ছে
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()  # Flask চালু করা
    try:
        bot.loop.run_until_complete(subsplease.on_new_anime(anime))
        bot.run()
    except KeyboardInterrupt:
        subsplease._exit()
