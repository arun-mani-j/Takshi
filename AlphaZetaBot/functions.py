import datetime
import logging
import os
import time
import telegram

from .message import Message


def format_text(user, chat_id, text):

    ftext = f"{user.id} @{user.username} {user.first_name} {user.last_name}\n{chat_id}\n{text}"
    return ftext


def get_configuration():

    config = {
        "ADMINS": [int(id.strip()) for id in os.getenv("ADMINS", "").strip("[]").split(",") if id.strip()],
        "CLEAN_INTERVAL": int(os.getenv("CLEAN_INTERVAL", "300")),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "GATEWAY": int(os.getenv("GATEWAY", "0")),
        "GROUP": int(os.getenv("GROUP", "0")),
        "INVITE_LINK": os.getenv("INVITE_LINK"),
        "MODERATE": int(os.getenv("MODERATE", "0")),
        "PORT": int(os.getenv("PORT")),
        "REFRESH_INTERVAL": int(os.getenv("REFRESH_INTERVAL", "24")),
        "SEND_LINK": f"https://t.me/{os.getenv('BOT_NAME')}?start=sendlink",
        "TOKEN": os.getenv("TOKEN"),
        "URL": os.getenv("URL"),
    }

    return config


def get_user_chat_ids(text):

    splits = text.split()
    return splits[0], splits[4]


def refresh_invite_link(context):

    context["INVITE_LINK"] = context.bot.export_chat_invite_link(
        chat_id=context["GROUP"]
    )


def remind_unapproved_users(context):

    bot = context.bot
    processor = context["processor"]

    unapproved = processor.get_unapproved_users()
    notify_msg = " ".join(
        f"[{i}](tg://user?id={user_id})" for i, user_id in enumerate(unapproved)
    )
    msg = bot.send_message(
        chat_id=context["GATEWAY"],
        text=notify_msg,
        parse_mode=telegram.ParseMode.Markdown,
    )
    msg.edit_text(text=Message.REMIND_UNAPPROVED_USERS)
    bot.send_message(
        chat_id=context["MODERATE"], text=Message.REMINDED_UNAPPROVED_USERS
    )


def remove_expired_users(context):

    logger = logging.getLogger()

    bot = context.bot
    processor = context["processor"]

    limit = datetime.now() - datetime.timedelta(context["CLEAN_INTERVAL"])

    expired_users = processor.get_expired_users(limit)
    count = 0
    for user_id in expired_users:
        try:
            bot.kick_chat_member(user_id=user_id, chat_id=context["GATEWAY"])
        except telegram.TelegramError as e:
            logger.error(e)
        else:
            count += 1

    bot.send_message(
        chat_id=context["MODERATE"],
        text=Message.REMOVED_EXPIRED_USERS.format(COUNT=count),
    )


def remove_joined_users_from_gateway(bot, gateway_id, *user_ids):

    logger = logging.getLogger()

    for user_id in user_ids:
        try:
            bot.kick_chat_member(
                chat_id=gateway_id, user_id=user_id, until_date=time.time() + 60
            )
        except telegram.TelegramError as e:
            logger.error(e)
