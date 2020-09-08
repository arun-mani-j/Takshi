import logging
import telegram

from .create_session import CreateSession
from .functions import (
    refresh_invite_link,
    remind_unapproved_users,
    remove_users_from_chat,
    remove_outdated_users,
)
from .join_session import JoinSession
from .constants import Label, Message
from .settings_session import SettingsSession
from .wrappers import (
    cache_group,
    check_is_group_message,
    check_is_private_message,
    check_is_reply,
    check_rights,
    check_valid_group,
)


@cache_group
@check_valid_group
@check_is_group_message
@check_rights
@check_is_reply
def approve_user(update, context):

    bot = context.bot
    cache = context.bot_data["cache"]
    processor = context.bot_data["processor"]
    message = update.message
    chat = message.chat
    reply = message.reply_to_message
    id, type = cache[chat.id]

    if type == 1:
        processor.approve_user(id, reply.from_user.id)
        message.delete()
        button = telegram.InlineKeyboardButton(
            text=Label.GET_LINK, url=f"{bot.link}?start=join={id}"
        )
        markup = telegram.InlineKeyboardMarkup.from_button(button)
        reply.reply_text(
            text=Message.PM_FOR_LINK,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=markup,
        )
    elif type == 2:
        try:
            user_id = int(reply.text.split("\n", 1)[0].split(":")[1].strip())
        except (ValueError, IndexError):
            message.reply_text(
                text=Message.INVALID_FORWARD, parse_mode=telegram.ParseMode.HTML
            )
        else:
            title = processor.get_title(id)
            processor.approve_user(id, user_id)
            text = Message.APPROVED_JOIN.format(TITLE=title)
            bot.send_message(
                chat_id=user_id, text=text, parse_mode=telegram.ParseMode.HTML
            )
            message.reply_text(
                text=Message.SENT_LINK, parse_mode=telegram.ParseMode.HTML
            )
    else:
        message.reply_text(
            text=Message.INVALID_COMMAND, parse_mode=telegram.ParseMode.HTML
        )


@cache_group
@check_valid_group
@check_is_group_message
@check_rights
@check_is_reply
def clear_messages(update, context):

    bot = context.bot
    chat = update.message.chat
    to_id = update.message.message_id
    from_id = update.message.reply_to_message.message_id

    for msg_id in range(from_id, to_id + 1):
        try:
            bot.delete_message(chat_id=chat.id, message_id=msg_id)
        except telegram.TelegramError as e:
            logging.error(e)


@cache_group
@check_valid_group
@check_is_group_message
@check_rights
def clean_outdated_users(update, context):

    bot = context.bot
    cache = context.bot_data["cache"]
    processor = context.bot_data["processor"]
    message = update.message
    chat = message.chat
    id, type = cache[chat.id]

    if type in (1, 2):
        remove_outdated_users(id, bot, processor)
    else:
        message.reply_text(
            text=Message.INVALID_COMMAND, parse_mode=telegram.ParseMode.HTML
        )

    if type == 1:
        message.delete()


@check_is_private_message
def configure_group(update, context):

    message = update.message
    session = SettingsSession(message, context)
    context.user_data["session"] = session


@check_is_private_message
def create_group(update, context):

    message = update.message
    session = CreateSession(message, context)
    context.user_data["session"] = session


@cache_group
@check_valid_group
def handle_left_member(update, context):

    cache = context.bot_data["cache"]
    processor = context.bot_data["processor"]
    message = update.message
    chat = message.chat
    left_user = message.left_chat_member
    id, type = cache[chat.id]

    logging.info(f"Left {left_user.id} of {id} in {type}")

    if type == 1:
        message.delete()
        processor.remove_user_from_gateway(id, left_user.id)
    elif type == 3:
        message.delete()
        processor.remove_user_from_group(id, left_user.id)


@cache_group
@check_valid_group
def handle_message(update, context):

    bot = context.bot
    cache = context.bot_data["cache"]
    message = update.message
    chat = message.chat
    reply = message.reply_to_message
    _, type = cache[chat.id]

    if type == 2 and and reply and reply.from_user.id == bot.id:
        try:
            chat_id = int(reply.text.split("\n", 1)[0].split(":")[1].strip())
        except (ValueError, IndexError):
            message.reply_text(
                text=Message.INVALID_FORWARD, parse_mode=telegram.ParseMode.HTML
            )
        else:
            bot.send_message(
                chat_id=chat_id,
                text=message.text_html_urled,
                parse_mode=telegram.ParseMode.HTML,
            )
            message.reply_text(
                text=Message.SENT_MESSAGE, parse_mode=telegram.ParseMode.HTML
            )


def handle_private_message(update, context):

    message = update.message
    session = context.user_data.get("session", None)

    if session:
        session.handle_message(message, context)
    else:
        message.reply_text(
            text=Message.INVALID_MESSAGE, parse_mode=telegram.ParseMode.HTML
        )


def handle_query(update, context):

    query = update.callback_query
    session = context.user_data.get("session", None)

    if session:
        session.handle_callback(query, context)
    else:
        query.answer()
        query.message.chat.send_message(
            text=Message.INVALID_QUERY, parse_mode=telegram.ParseMode.HTML
        )


@cache_group
@check_valid_group
def handle_new_member(update, context):

    bot = context.bot
    cache = context.bot_data["cache"]
    processor = context.bot_data["processor"]
    message = update.message
    chat = message.chat
    new_members = message.new_chat_members
    user_ids = [user.id for user in new_members]
    id, type = cache[chat.id]

    if type == 1:
        processor.add_users_to_gateway(id, *user_ids)
        message.delete()
    elif type == 3:
        processor.add_users_to_group(id, *user_ids)
        message.delete()
        remove_users_from_chat(user_ids, chat.id, bot)
        for user_id in user_ids:
            processor.remove_user_from_gateway(id, user_id)


@cache_group
@check_valid_group
@check_is_group_message
@check_rights
@check_is_reply
def ignore_user(update, context):

    bot = context.bot
    cache = context.bot_data["cache"]
    processor = context.bot_data["processor"]
    message = update.message
    chat = message.chat
    reply = message.reply_to_message
    id, type = cache[chat.id]
    moderate_id = processor.get_moderate_id(id)

    if type in (1, 3):
        processor.ignore_user(id, reply.from_user.id)
        message.delete()
        bot.send_message(
            chat_id=moderate_id,
            text=Message.IGNORED_USER,
            parse_mode=telegram.ParseMode.HTML,
        )

    elif type == 2:
        try:
            user_id = int(reply.text.split("\n", 1)[0].split(":")[1].strip())
        except (ValueError, IndexError):
            message.reply_text(
                text=Message.INVALID_FORWARD, parse_mode=telegram.ParseMode.HTML
            )
        else:
            processor.ignore_user(id, user_id)
            message.reply_text(
                text=Message.IGNORED_USER, parse_mode=telegram.ParseMode.HTML
            )


@check_is_private_message
def join_group(update, context):

    message = update.message
    session = JoinSession(message, context)
    context.user_data["session"] = session


@cache_group
@check_valid_group
@check_is_group_message
@check_rights
def remind_users(update, context):

    bot = context.bot
    cache = context.bot_data["cache"]
    processor = context.bot_data["processor"]
    message = update.message
    chat = message.chat
    id, type = cache[chat.id]

    if type in (1, 2):
        remind_unapproved_users(id, bot, processor)
    else:
        message.reply_text(
            text=Message.INVALID_COMMAND, parse_mode=telegram.ParseMode.HTML
        )

    if type == 1:
        message.delete()


@cache_group
@check_valid_group
@check_is_group_message
@check_rights
@check_is_reply
def request_explanation(update, context):

    bot = context.bot
    cache = context.bot_data["cache"]
    processor = context.bot_data["processor"]
    message = update.message
    chat = message.chat
    reply = message.reply_to_message
    id, type = cache[chat.id]
    prompt = processor.get_prompt(id)

    if type == 1:
        message.delete()
        reply.reply_text(text=prompt, parse_mode=telegram.ParseMode.HTML)
    elif type == 2:
        try:
            chat_id = int(reply.text.split("\n", 1)[0].split(":")[1].strip())
        except (ValueError, IndexError):
            message.reply_text(
                text=Message.INVALID_FORWARD, parse_mode=telegram.ParseMode.HTML
            )
        else:
            bot.send_message(
                chat_id=chat_id, text=prompt, parse_mode=telegram.ParseMode.HTML
            )
            message.reply_text(
                text=Message.SENT_EXPLANATION, parse_mode=telegram.ParseMode.HTML
            )
    else:
        message.reply_text(
            text=Message.INVALID_COMMAND, parse_mode=telegram.ParseMode.HTML
        )


@cache_group
@check_valid_group
@check_is_group_message
@check_rights
@check_is_reply
def restrict_user(update, context):

    bot = context.bot
    cache = context.bot_data["cache"]
    processor = context.bot_data["processor"]
    message = update.message
    chat = message.chat
    reply = message.reply_to_message
    id, type = cache[chat.id]

    if type == 1:
        processor.restrict_user(id, reply.from_user.id)
        reply.delete()
        message.delete()
        chat.kick_member(user_id=reply.from_user.id)
        processor.remove_from_gateway(id, reply.from_user.id)
    elif type == 2:
        try:
            user_id = int(reply.text.split("\n", 1)[0].split(":")[1].strip())
        except (ValueError, IndexError):
            message.reply_text(
                text=Message.INVALID_FORWARD, parse_mode=telegram.ParseMode.HTML
            )
        else:
            processor.restrict_user(id, user_id)
            gateway_id, _, group_id = processor.get_chat_ids(id)
            bot.kick_chat_member(chat_id=gateway_id, user_id=user_id)
            bot.kick_chat_member(chat_id=group_id, user_id=user_id)
            processor.remove_from_gateway(id, user_id)
            processor.remove_from_group(id, user_id)
            message.reply_text(
                text=Message.RESTRICTED_USER, parse_mode=telegram.ParseMode.HTML
            )
    elif type == 3:
        processor.restrict_user(id, reply.from_user.id)
        reply.delete()
        message.delete()
        chat.kick_member(user_id=reply.from_user.id)
        processor.remove_from_group(id, user_id)


@cache_group
@check_valid_group
@check_is_group_message
@check_rights
def revoke_link(update, context):

    bot = context.bot
    cache = context.bot_data["cache"]
    processor = context.bot_data["processor"]
    message = update.message
    chat = message.chat
    id, type = cache[chat.id]

    refresh_invite_link(id, bot, processor)

    if type in (1, 3):
        message.delete()
    chat.send_message(text=Message.REVOKED_LINK, parse_mode=telegram.ParseMode.HTML)


def send_help(update, context):

    message = update.message
    chat = message.chat

    if chat.type == "private":
        message.reply_text(
            text=Message.HELP,
            parse_mode=telegram.ParseMode.HTML,
            disable_web_page_preview=True,
        )
    else:
        message.reply_text(text=Message.HELP_IN_PM, parse_mode=telegram.ParseMode.HTML)


def send_id(update, context):

    message = update.message
    chat = message.chat
    reply = message.reply_to_message
    user_id = reply.from_user.id if reply else message.from_user.id
    text = Message.CHAT_ID.format(CHAT_ID=chat.id, USER_ID=user_id)

    message.reply_text(text=text, parse_mode=telegram.ParseMode.HTML)


@cache_group
@check_valid_group
@check_is_group_message
@check_rights
@check_is_reply
def send_link(update, context):

    bot = context.bot
    cache = context.bot_data["cache"]
    processor = context.bot_data["processor"]
    message = update.message
    reply = message.reply_to_message
    chat = message.chat
    id, type = cache[chat.id]

    if type == 1:
        message.delete()
        button = telegram.InlineKeyboardButton(
            text=Label.GET_LINK, url=f"{bot.link}?start=join={id}"
        )
        markup = telegram.InlineKeyboardMarkup.from_button(button)
        reply.reply_text(
            text=Message.PM_FOR_LINK,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=markup,
        )
    elif type == 2:
        try:
            chat_id = int(reply.text.split("\n", 1)[0].split(":")[1].strip())
        except (ValueError, IndexError):
            message.reply_text(
                text=Message.INVALID_FORWARD, parse_mode=telegram.ParseMode.HTML
            )
        else:
            title = processor.get_title(id)
            text = Message.APPROVED_JOIN.format(TITLE=title)
            bot.send_message(
                chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML
            )
            message.reply_text(
                text=Message.SENT_LINK, parse_mode=telegram.ParseMode.HTML
            )
    else:
        message.reply_text(
            text=Message.INVALID_COMMAND, parse_mode=telegram.ParseMode.HTML
        )


def send_start(update, context):

    args = context.args
    message = update.message
    chat = message.chat
    session = context.user_data.get("session", None)

    if chat.type == "private" and args:
        if args[0].startswith("join="):
            session = JoinSession(message, context)
            context.user_data["session"] = session
        else:
            chat.send_message(
                Message.INVALID_START_ARG, parse_mode=telegram.ParseMode.HTML
            )
    elif chat.type == "private" and not args:
        chat.send_message(text=Message.START, parse_mode=telegram.ParseMode.HTML)
    elif chat.type != "private" and args:
        if session:
            session.handle_start(message, context)
        else:
            chat.send_message(
                Message.INVALID_START_ARG, parse_mode=telegram.ParseMode.HTML
            )
    else:
        chat.send_message(text=Message.START_GROUP, parse_mode=telegram.ParseMode.HTML)
