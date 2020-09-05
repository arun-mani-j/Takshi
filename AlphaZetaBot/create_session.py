import logging
import telegram

from .constants import Label, Message
from .functions import get_admins
from .session import Session


class CreateSession(Session):
    def __init__(self, message, context):

        Session.__init__(self, message, context)
        self.base_message = None
        self.chats = [None, None, None]
        self.create_allowed = context["ALLOW_CREATE"]
        self.send_select_group()

    def do_create_group(self):

        if not self.chats[0]:
            return Message.SELECT_GATEWAY

        if not self.chats[1]:
            return Message.SELECT_MODERATE

        if not self.chats[2]:
            return Message.SELECT_PRIVATE_GROUP

        gateway, moderate, priv_group = self.chats
        admins = get_admins([gateway.id, moderate.id, priv_group.id])
        title = priv_group.title
        id = self.processor.add_group(
            title, gateway.id, moderate.id, priv_group.id, admins
        )

        if not id:
            self.base_message.edit_text(
                text=Message.GROUP_EXISTS, parse_mode=telegram.ParseMode.HTML
            )
        else:
            self.base_message.edit_text(
                text=Message.GROUP_CREATED.format(TITLE=title),
                parse_mode=telegram.ParseMode.HTML,
            )

        return Message.DONE

    def handle_callback(self, query, context):

        data = query.data

        if data == "createGroup":
            text = self.do_create_group()
            query.answer(text=text, show_alert=True)
        elif not data:
            query.answer()
        else:
            logging.critical(f"Unexpected query with data {data}")
            query.answer(text=Message.INVALID_QUERY, show_alert=True)

    def handle_start(self, message, context):

        if "selectGateway" in context.args:
            self.chats[0] = message.chat
            message.reply_text(
                text=Message.SELECTED_GATEWAY, parse_mode=telegram.ParseMode.HTML
            )
        elif "selectModerate" in context.args:
            self.chats[1] = message.chat
            message.reply_text(
                text=Message.SELECTED_MODERATE, parse_mode=telegram.ParseMode.HTML
            )
        elif "selectPrivate" in context.args:
            self.chats[2] = message.chat
            message.reply_text(
                text=Message.SELECTED_PRIVATE_GROUP, parse_mode=telegram.ParseMode.HTML
            )
        else:
            logging.critical(f"Start arguments are invalid : {context.args}")
            message.reply_text(
                text=Message.INVALID_START_ARG, parse_mode=telegram.ParseMode.HTML
            )

    def send_select_group(self):

        if not self.create_allowed:
            self.chat.send_message(
                text=Message.CREATE_NOT_ALLOWED, parse_mode=telegram.ParseMode.HTML
            )
            return

        start_link = f"{self.bot.link}?startgroup=select"

        buttons = [
            [
                telegram.InlineKeyboardButton(
                    text=Label.SELECT_GATEWAY, callback_data=f"{start_link}Gateway"
                ),
                telegram.InlineKeyboardButton(
                    text=Label.SELECT_MODERATE, callback_data=f"{start_link}Moderate"
                ),
                telegram.InlineKeyboardButton(
                    text=Label.SELECT_PRIVATE_GROUP,
                    callback_data=f"{start_link}Private",
                ),
            ],
            [
                telegram.InlineKeyboardButton(
                    text=Label.CONFIRM, callback_data="createGroup"
                )
            ],
        ]

        markup = telegram.InlineKeyboardMarkup(buttons)
        self.chat.send_message(
            text=Message.CREATE_BANNER,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=markup,
        )
