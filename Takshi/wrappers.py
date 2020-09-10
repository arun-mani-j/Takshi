import telegram
from .constants import Message
from .processor import Processor


def cache_group(func):
    def wrapped(update: telegram.Update, context: CallbackContext):

        cache: dict = context.bot_data["cache"]
        processor: Processor = context.bot_data["processor"]
        message: telegram.Message = update.message
        chat: telegram.Chat = message.chat

        try:
            cache[chat.id]
        except KeyError:
            cache[chat.id] = processor.find_id(chat.id)

        func(update, context)

    return wrapped


def check_is_group_message(func):
    def wrapped(update: telegram.Update, context: CallbackContext):

        message: telegram.Message = update.message
        chat: telegram.Chat = message.chat

        if chat.type != "private":
            func(update, context)
        else:
            message.reply_text(Message.GROUP_COMMAND)

    return wrapped


def check_is_private_message(func):
    def wrapped(update: telegram.Update, context: CallbackContext):

        message: telegram.Message = update.message
        chat: telegram.Chat = message.chat

        if chat.type == "private":
            func(update, context)
        else:
            message.reply_text(Message.PM_COMMAND)

    return wrapped


def check_is_reply(func):
    def wrapped(update: telegram.Update, context: CallbackContext):

        message: telegram.Message = update.message

        if message.reply_to_message:
            func(update, context)
        else:
            message.reply_text(Message.INVALID_REPLY)

    return wrapped


def check_rights(func):
    def wrapped(update: telegram.Update, context: CallbackContext):

        cache: dict = context.bot_data["cache"]
        processor: Processor = context.bot_data["processor"]
        message: telegram.Message = update.message
        chat: telegram.Chat = message.chat
        user: telegram.User = message.from_user

        id, _ = cache[chat.id]
        allowed = processor.is_admin(id, user.id)

        if message and allowed:
            func(update, context)
        else:
            message.reply_text(Message.INVALID_COMMAND)

    return wrapped


def check_valid_group(func):
    def wrapped(update: telegram.Update, context: CallbackContext):

        cache: dict = context.bot_data["cache"]
        message: telegram.Message = update.message
        chat: telegram.Chat = message.chat
        id, type = cache[chat.id]

        if id and type:
            func(update, context)
        else:
            message.reply_text(
                text=Message.INVALID_GROUP, parse_mode=telegram.ParseMode.HTML
            )

    return wrapped
