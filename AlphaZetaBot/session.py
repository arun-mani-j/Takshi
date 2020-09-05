import telegram
from .constants import Message


class Session:
    def __init__(self, message, context):

        self.bot = context.bot
        self.chat = message.chat
        self.processor = context["processor"]
        self.user = message.from_user

    def __del__(self):

        self.expire()

    def expire(self, continued=True):

        if self.base_message:
            if continued:
                self.base_message.edit_text(
                    text=Message.SESSION_CONTINUED, parse_mode=telegram.ParseMode.HTML
                )
            else:
                self.base_message.edit_text(
                    text=Message.SESSION_EXPIRED, parse_mode=telegram.ParseMode.HTML
                )

    def handle_callback(self, query, context):

        self.chat.send_message(
            text=Message.INVALID_QUERY, parse_mode=telegram.ParseMode.HTML
        )

    def handle_message(self, message, context):

        self.chat.send_message(
            text=Message.INVALID_MESSAGE, parse_mode=telegram.ParseMode.HTML
        )

    def handle_start(self, message, context):

        self.chat.send_message(
            text=Message.INVALID_START_ARG, parse_mode=telegram.ParseMode.HTML
        )
