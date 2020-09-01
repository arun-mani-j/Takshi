import logging
import telegram

from .functions import (
    format_text,
    get_user_chat_ids,
    refresh_invite_link,
    remove_joined_users_from_gateway,
)
from .wrappers import check_is_reply, check_rights
from .message import Message


@check_rights
@check_is_reply
def approve_user(update, context):

    bot = context.bot
    processor = context["processor"]

    message = update.message
    reply = message.reply_to_message
    chat = message.chat

    if chat.id == context["GATEWAY"]:
        processor.approve_user(reply.from_user.id)
        button = telegram.InlineKeyboardButton(
            text=Message.LABEL_GET_LINK, url=context["START_LINK"]
        )
        markup = telegram.InlineKeyboardMarkup.from_button(button)
        message.delete()
        reply.send_text(
            text=Message.PM_FOR_LINK,
            reply_markup=markup,
            parse_mode=telegram.ParseMode.MARKDOWN_V2,
        )

    elif chat.id == context["MODERATE"]:
        user_id, chat_id = get_user_chat_ids(reply.text)
        processor.approve_user(user_id)
        button = telegram.InlineKeyboardButton(
            text=Message.LABEL_JOIN_LINK, url=context["INVITE_LINK"]
        )
        markup = telegram.InlineKeyboardMarkup.from_button(button)
        bot.send_message(
            chat_id=chat_id,
            text=Message.LINK_CAUTION,
            reply_markup=markup,
            parse_mode=telegram.ParseMode.MARKDOWN_V2,
        )
        message.reply_text(text=Message.SENT_LINK)


@check_rights
@check_is_reply
def clear_messages(update, context):

    logger = logging.getLogger()
    bot = context.bot

    chat_id = update.message.chat.id
    from_id = update.message.id
    to_id = update.message.reply_to_message.id

    for msg_id in range(from_id, to_id):
        try:
            bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except telegram.TelegramError as e:
            logger.error(e)


def handle_left_member(update, context):

    processor = context["processor"]

    message = update.message
    chat = message.chat
    left_user = message.left_chat_member

    if chat.id == context["GATEWAY"]:
        processor.remove_user_from_gateway(left_user.id)
    elif chat.id == context["GROUP"]:
        processor.remove_user_from_group(left_user.id)


def handle_private_message(update, context):

    message = update.message
    bot = context.bot
    chat = message.chat
    user = message.user

    text = format_text(user, chat.id, message.text)
    bot.send_message(chat_id=context["MODERATE"], text=text)


def handle_query(update, context):

    update.callback_query.answer()


def handle_reply_message(update, context):

    message = update.message
    bot = context.bot
    chat = message.chat

    reply = message.reply
    if reply.from_user != bot and chat.id != context["MODERATE"]:
        return

    user_id, chat_id = get_user_chat_ids(reply.text)
    bot.send_message(
        chat_id=chat_id, text=message.text, parse_mode=telegram.ParseMode.MARKDOWN_V2
    )
    message.reply_text(text=Message.SENT_TEXT_MESSAGE)


def handle_new_member(update, context):

    bot = context.bot
    processor = context["processor"]

    message = update.message
    chat = message.chat
    new_users = message.new_chat_members
    new_user_ids = [user.id for user in new_users]

    if chat.id == context["GATEWAY"]:
        processor.add_user_to_gateway(*new_user_ids)
    elif chat.id == context["GROUP"]:
        processor.add_user_to_group(*new_user_ids)
        remove_joined_users_from_gateway(bot, context["GATEWAY"], new_user_ids)


@check_rights
@check_is_reply
def request_explanation(update, context):

    bot = context.bot

    message = update.message
    reply = message.reply_to_message
    chat = message.chat

    if chat.id == context["GATEWAY"]:
        message.delete()
        reply.send_text(
            text=Message.REQUEST_EXPLANATION, parse_mode=telegram.ParseMode.MARKDOWN_V2
        )
    elif chat.id == context["GROUP"]:
        user_id, chat_id = get_user_chat_ids(reply.text)
        bot.send_message(
            chat_id=chat_id,
            text=Message.REQUEST_EXPLANATION,
            parse_mode=telegram.ParseMode.MARKDOWN_V2,
        )
        message.reply_text(Message.SENT_REQUEST_EXPLANATION)


@check_rights
@check_is_reply
def restrict_user(update, context):

    bot = context.bot
    processor = context["processor"]

    message = update.message
    reply = message.reply_to_message
    chat = message.chat

    if chat.id == context["GATEWAY"]:
        processor.restrict_user(reply.from_user.id)
        bot.kick_chat_member(chat_id=chat.id, user_id=reply.from_user.id)
        reply.delete()
        message.delete()
    elif chat.id == context["MODERATE"]:
        user_id, chat_id = get_user_chat_ids(reply.text)
        bot.kick_chat_member(chat_id=context["GATEWAY"], user_id=user_id)
        processor.restrict_user(user_id)
        message.reply_text(
            text=Message.REMOVED_USER, parse_mode=telegram.ParseMode.MARKDOWN_V2
        )


@check_rights
def revoke_link(update, context):

    bot = context.bot

    message = update.message
    chat = message.chat

    if chat.id == context["GATEWAY"]:
        message.delete()

    refresh_invite_link(context)
    bot.send_message(chat_id=context["MODERATE"], text=Message.REVOKED_LINK)


def send_id(update, context):

    message = update.message
    chat = message.chat
    user = message.user

    text = f"Chat ID : {chat.id}\n User ID : {user.id}"
    message.reply_text(text=text)


def send_link(update, context):

    bot = context.bot
    processor = context["processor"]

    message = update.message
    reply = message.reply_to_message
    chat = message.chat
    user = message.from_user

    if chat.type == "private":
        ret = processor.get_user_eligible_for_link(user.id)
        if ret == -1:
            message.send_text(
                text=Message.UNAPPROVED_USER, parse_mode=telegram.ParseMode.MARKDOWN_V2
            )
        elif ret == 0:
            button = telegram.InlineKeyboardButton(
                Message.LABEL_JOIN_LINK, url=context["INVITE_LINK"]
            )
            markup = telegram.InlineKeyboardMarkup.from_button(button)
            message.send_text(
                Message.LINK_CAUTION,
                reply_markup=markup,
                parse_mode=telegram.ParseMode.MARKDOWN_V2,
            )
        elif ret == 1:
            message.send_text(
                text=Message.ALREADY_JOINED, parse_mode=telegram.ParseMode.MARKDOWN_V2
            )
    elif chat.id == context["GATEWAY"]:
        processor.approve_user(reply.from_user.id)
        button = telegram.InlineKeyboardButton(
            Message.LABEL_GET_LINK, url=context["START_LINK"]
        )
        markup = telegram.InlineKeyboardMarkup.from_button(button)
        message.delete()
        reply.send_text(Message.PM_FOR_LINK, reply_markup=markup)
    elif chat.id == context["MODERATE"]:
        user_id, chat_id = get_user_chat_ids(reply.text)
        processor.approve_user(user_id)
        button = telegram.InlineKeyboardButton(
            Message.LABEL_JOIN_LINK, url=context["INVITE_LINK"]
        )
        markup = telegram.InlineKeyboardMarkup.from_button(button)
        bot.send_message(
            Message.LINK_CAUTION,
            chat_id=chat_id,
            reply_markup=markup,
            parse_mode=telegram.ParseMode.MARKDOWN_V2,
        )
        message.reply_text(Message.SENT_LINK)


def send_start(update, context):

    message = update.message
    if context.args:
        send_link(update, context)
    else:
        message.send_text(Message.START)
