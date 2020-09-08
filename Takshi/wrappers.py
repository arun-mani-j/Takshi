import telegram
from .constants import Message


def cache_group(func):
    def wrapped(update, context):

        cache = context.bot_data["cache"]
        processor = context.bot_data["processor"]
        message = update.message
        chat = message.chat

        try:
            cache[chat.id]
        except KeyError:
            cache[chat.id] = processor.find_id(chat.id)

        func(update, context)

    return wrapped


def check_is_group_message(func):
    def wrapped(update, context):

        message = update.message
        chat = message.chat

        if chat.type != "private":
            func(update, context)
        else:
            message.reply_text(Message.GROUP_COMMAND)

    return wrapped


def check_is_private_message(func):
    def wrapped(update, context):

        message = update.message
        chat = message.chat

        if chat.type == "private":
            func(update, context)
        else:
            message.reply_text(Message.PM_COMMAND)

    return wrapped


def check_is_reply(func):
    def wrapped(update, context):

        message = update.message

        if message.reply_to_message:
            func(update, context)
        else:
            message.reply_text(Message.INVALID_REPLY)

    return wrapped


def check_rights(func):
    def wrapped(update, context):

        cache = context.bot_data["cache"]
        processor = context.bot_data["processor"]
        message = update.message
        chat = message.chat
        user = message.from_user

        id, _ = cache[chat.id]
        allowed = processor.is_admin(id, user.id)

        if message and allowed:
            func(update, context)
        else:
            message.reply_text(Message.INVALID_COMMAND)

    return wrapped


def check_valid_group(func):
    def wrapped(update, context):

        cache = context.bot_data["cache"]
        message = update.message
        chat = message.chat
        id, type = cache[chat.id]

        if id and type:
            func(update, context)
        else:
            message.reply_text(
                text=Message.INVALID_GROUP, parse_mode=telegram.ParseMode.HTML
            )

    return wrapped
