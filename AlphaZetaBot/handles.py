from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from telegram.ext import Filters

from .handlers import (
    approve_user,
    clear_messages,
    handle_left_member,
    handle_private_message,
    handle_query,
    handle_reply_message,
    handle_new_member,
    restrict_user,
    request_explanation,
    revoke_link,
    send_link,
    send_start,
)

handles = {
    CallbackQueryHandler: [(handle_query,), ()],
    CommandHandler: [
        (("/approve", approve_user), ()),
        (("/clear", clear_messages), ()),
        (("/explain", request_explanation), ()),
        (("/link", send_link), ()),
        (("/restrict", restrict_user), ()),
        (("/revoke", revoke_link), ()),
        (("/start", send_start, Filters.private), ()),
    ],
    MessageHandler: [
        ((handle_left_member, Filters.status_update.left_chat_member), ()),
        (
            (handle_private_message, Filters.text & ~Filters.command & Filters.private),
            (),
        ),
        ((handle_reply_message, Filters.text & ~Filters.command & Filters.reply), ()),
        ((handle_new_member, Filters.status_update.new_chat_members), ()),
    ],
}
