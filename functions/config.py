#    This file is part of the AutoAnime distribution.
#    Copyright (c) 2025 Kaif_00z
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in <
# https://github.com/kaif-00z/AutoAnimeBot/blob/main/LICENSE > .

# if you are using this following code then don't forgot to give proper
# credit to t.me/kAiF_00z (github.com/kaif-00z)

from decouple import config


class Var:
    # Version

    __version__ = "v0.1@stable.july"

    # Telegram Credentials

    API_ID = config("API_ID", default=6, cast=int)
    API_HASH = config("API_HASH", default="eb06d4abfb49dc3eeb1aeb98ae0f581e")
    BOT_TOKEN = config("BOT_TOKEN", default=None)
    SESSION = config("SESSION", default=None)

    # Database Credentials

    MONGO_SRV = config("MONGO_SRV", default=mongodb+srv://rohanahamed75:gt4RXJZ1mUtOh4Xv@mmtg.0ong5.mongodb.net/?retryWrites=true&w=majority&appName=mmtg)

    # Channels Ids

    BACKUP_CHANNEL = config("BACKUP_CHANNEL", default=-1002546594659, cast=int)
    MAIN_CHANNEL = config("MAIN_CHANNEL", default=-1002401440098, cast=int)
    LOG_CHANNEL = config("LOG_CHANNEL", default=-1002437314123, cast=int)
    CLOUD_CHANNEL = config("CLOUD_CHANNEL", default=-1002546594659, cast=int)
    FORCESUB_CHANNEL = config("FORCESUB_CHANNEL", default=-1002394229067, cast=int)
    OWNER = config("OWNER", default=0, default=7822720438, cast=int)

    # Other Configs

    THUMB = config(
        "THUMBNAIL",
        default="https://graph.org/file/d4e6d1fd7e7fde9bee166-42d4b966221d9fe0c3.jpg",
    )
    FFMPEG = config("FFMPEG", default="ffmpeg")
    CRF = config("CRF", default="27")
    SEND_SCHEDULE = config("SEND_SCHEDULE", default=True, cast=bool)
    RESTART_EVERDAY = config("RESTART_EVERDAY", default=False, cast=bool)
    LOG_ON_MAIN = config("LOG_ON_MAIN", default=True, cast=bool)
    FORCESUB_CHANNEL_LINK = config("FORCESUB_CHANNEL_LINK", default="https://t.me/AnimeTaboo", cast=str)

    # Dev Configs

    DEV_MODE = config("DEV_MODE", default=False, cast=bool)
