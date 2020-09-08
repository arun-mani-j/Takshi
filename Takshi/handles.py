from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from telegram.ext import Filters

from .handlers import (
    approve_user,
    clean_outdated_users,
    clear_messages,
    configure_group,
    create_group,
    handle_left_member,
    handle_message,
    handle_private_message,
    handle_query,
    handle_new_member,
    ignore_user,
    join_group,
    remind_users,
    restrict_user,
    request_explanation,
    revoke_link,
    send_help,
    send_id,
    send_link,
    send_start,
)

handles = {
    CallbackQueryHandler: [((handle_query,), ()),],
    CommandHandler: [
        (("approve", approve_user), ()),
        (("create", create_group), ()),
        (("clean", clean_outdated_users,), ()),
        (("clear", clear_messages), ()),
        (("explain", request_explanation), ()),
        (("help", send_help), ()),
        (("id", send_id), ()),
        (("ignore", ignore_user), ()),
        (("join", join_group), ()),
        (("link", send_link), ()),
        (("remind", remind_users), ()),
        (("restrict", restrict_user), ()),
        (("revoke", revoke_link), ()),
        (("settings", configure_group), ()),
        (("start", send_start), ()),
    ],
    MessageHandler: [
        ((Filters.status_update.left_chat_member, handle_left_member), ()),
        ((Filters.status_update.new_chat_members, handle_new_member), ()),
        (
            (Filters.text & ~Filters.command & Filters.private, handle_private_message),
            (),
        ),
        ((Filters.text & ~Filters.command, handle_message), ()),
    ],
}
