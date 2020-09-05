import datetime
import logging
import time
import telegram

from .message import Message


def get_admins(chat_ids, bot):

    admins = []
    for chat_id in chat_ids:
        chat_admins = bot.get_chat_administrators(chat_id=chat_id)
        admins.extend(chat_admins)
    return list(set(admins))


def get_user_chat_ids(text):

    splits = text.splitlines()
    user_id = splits[0].split(":")[-1]
    chat_id = splits[3].split(":")[-1]
    return (user_id, chat_id)


def refresh_invite_link(id, bot, processor):

    priv_group_id = processor.get_private_group_id(id)
    link = bot.export_chat_invite_link(chat_id=priv_group_id)
    processor.set_invite_link(id, link)


def remind_unapproved_users(id, before_date, bot, processor):

    gateway_id = processor.get_gateway_id(id)
    unapproved = processor.get_unapproved_users(id, before_date)

    notify_msg = " ".join(Message.MENTION.format(CAPTION=i, USER_ID=user_id) for i, user_id in enumerate(unapproved))
    msg = bot.send_message(chat_id=gateway_id, text=notify_msg, parse_mode=telegram.ParseMode.HTML)
    msg.edit_text(text=Message.REMIND_UNAPPROVED_USERS)


def remove_expired_users(id, before_date, bot, processor):

    gateway_id = processor.get_gateway_id(id)
    moderate_id = processor.get_moderate_id(id)
    expired_users = processor.get_unapproved_users(id, before_date)
    count = 0

    for user_id in expired_users:
        try:
            bot.kick_chat_member(user_id=user_id, chat_id=gateway_id)
        except telegram.TelegramError as e:
            logger.error(e)
        else:
            count += 1

    bot.send_message(chat_id=moderate_id, text=Message.REMOVED_EXPIRED_USERS.format(COUNT=count), parse_mode=telegram.ParseMode.HTML)


def periodic_job(context):

    bot context.bot
    processor = context["processor"]
    intevals = context["intevals"]

    for _ in range(len(intevals)):
        id, cln_int, cur_cln_val, ref_int, cur_ref_val = intevals.pop(0)

        if cur_cln_val == cln_int // 2:
            before_date = datetime.datetime.now() - datetime.timedelta(minutes=cln_int // 2)
            remind_unapproved_users(id, before_date, bot, processor)
        elif cur_cln_val == cln_int:
            before_date = datetime.datetime.now() - datetime.timedelta(minutes=cln_int)
            remove_expired_users(id, before_date, bot, processor)
            cur_cln_val = 0
        cur_cln_val += 1

        if cur_ref_val == ref_int:
            refresh_invite_link(id, bot, processor)
            cur_ref_val = 0
        cur_ref_val += 1

        intervals.append((id, cln_int, cur_cln_val, ref_int, cur_ref_val))
