from .message import Message


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

        message = update.message
        user = message.from_user

        if message and user.id in context["ADMINS"]:
            func(update, context)
        else:
            message.reply_text(Message.BAD_COMMAND)

    return wrapped
