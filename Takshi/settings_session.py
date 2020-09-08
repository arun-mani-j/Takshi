import logging
import telegram

from .constants import Label, Message
from .functions import get_admins, get_chat_title, leave_chats
from .session import Session


class SettingsSession(Session):
    def __init__(self, message, context):

        Session.__init__(self, message, context)
        self.editing_prop = None
        self.group_id = None
        self.group_title = None
        self.groups = self.processor.get_controlled_groups(self.user.id)
        self.send_select_group(edit=False)

    def do_delete_group(self):

        chat_ids = self.processor.get_chat_ids(self.group_id)
        leave_chats(chat_ids, self.bot)
        self.processor.delete_group(self.group_id)
        del self.groups[self.group_id]

    def do_change_clean_interval(self, interval):

        val = interval.strip()
        try:
            val = int(float(val))
            assert val > 0
        except (AssertionError, ValueError):
            self.editing_prop = "clean_interval"
            self.chat.send_message(
                text=Message.INVALID_INTERVAL, parse_mode=telegram.ParseMode.HTML
            )
        else:
            self.processor.set_clean_interval(self.group_id, val)
            self.expire(continued=True)
            text = Message.SET_CLEAN_INTERVAL.format(
                TITLE=self.group_title, INTERVAL=val
            )
            self.chat.send_message(text=text, parse_mode=telegram.ParseMode.HTML)
            self.send_select_property(edit=False)

    def do_change_prompt(self, prompt):

        prompt = prompt.strip()
        if prompt:
            self.processor.set_prompt(self.group_id, prompt)
            self.expire(continued=True)
            text = Message.SET_PROMPT.format(TITLE=self.group_title)
            self.chat.send_message(text=text, parse_mode=telegram.ParseMode.HTML)
            self.send_select_property(edit=False)
        else:
            self.editing_prop = "prompt"
            self.chat.send_message(
                text=Message.INVALID_PROMPT, parse_mode=telegram.ParseMode.HTML
            )

    def do_change_refresh_interval(self, interval):

        val = interval.strip()
        try:
            val = int(float(val))
            assert val > 0
        except (AssertionError, ValueError):
            self.editing_prop = "refresh_interval"
            self.chat.send_message(
                text=Message.INVALID_INTERVAL, parse_mode=telegram.ParseMode.HTML
            )
        else:
            self.processor.set_refresh_interval(self.group_id, val)
            self.expire(continued=True)
            text = Message.SET_REFRESH_INTERVAL.format(
                TITLE=self.group_title, INTERVAL=val
            )
            self.chat.send_message(text=text, parse_mode=telegram.ParseMode.HTML)
            self.send_select_property(edit=False)

    def handle_callback(self, query, context):

        data = query.data
        self.editing_prop = None

        if data == "delCfm":
            text = Message.GROUP_DELETED.format(TITLE=self.group_title)
            self.do_delete_group()
            query.answer(text=text, show_alert=True)
            self.send_select_group()
            return

        query.answer()

        if data == "selGrp":
            self.send_select_group()

        elif data.startswith("grp="):
            str_id = data.lstrip("grp=")
            try:
                self.group_id = int(str_id)
            except ValueError:
                logging.error(
                    "Non-integer value %s given for grp in Settings Session", str_id,
                )
                self.chat.send_message(
                    text=Message.INVALID_QUERY, parse_mode=telegram.ParseMode.HTML
                )
            else:
                self.group_title = self.groups[self.group_id]
                self.send_select_property()

        elif data == "selPrp":
            self.send_select_property()

        elif data == "delGrp":
            self.send_delete()

        elif data == "clnInt":
            self.send_change_clean_interval()

        elif data == "prt":
            self.send_change_prompt()

        elif data == "refInt":
            self.send_change_refresh_interval()

        elif data == "upd":
            self.send_update_data()

        else:
            logging.critical("Unexpected query %s in Settings Session", data)
            self.chat.send_message(
                text=Message.INVALID_QUERY, parse_mode=telegram.ParseMode.HTML
            )

    def handle_message(self, message, context):

        editing_prop = self.editing_prop
        self.editing_prop = None
        if editing_prop == "clean_interval":
            self.do_change_clean_interval(message.text)
        elif editing_prop == "prompt":
            self.do_change_prompt(message.text_html_urled)
        elif editing_prop == "refresh_interval":
            self.do_change_refresh_interval(message.text)
        else:
            message.reply_text(
                text=Message.INVALID_SESSION_MESSAGE, parse_mode=telegram.ParseMode.HTML
            )

    def send_change_clean_interval(self):

        self.editing_prop = "clean_interval"
        interval = self.processor.get_clean_interval(self.group_id)
        if not interval:
            self.send_group_not_found()
            return
        button = telegram.InlineKeyboardButton(text=Label.BACK, callback_data="selPrp")
        markup = telegram.InlineKeyboardMarkup.from_button(button)
        text = Message.SETTING_CLEAN_INTERVAL.format(
            TITLE=self.group_title, INTERVAL=interval
        )
        self.base_message.edit_text(
            text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=markup
        )

    def send_change_prompt(self):

        self.editing_prop = "prompt"
        prompt = self.processor.get_prompt(self.group_id)
        if not prompt:
            self.send_group_not_found()
            return
        button = telegram.InlineKeyboardButton(text=Label.BACK, callback_data="selPrp")
        markup = telegram.InlineKeyboardMarkup.from_button(button)
        text = Message.SETTING_PROMPT.format(TITLE=self.group_title, PROMPT=prompt)
        self.base_message.edit_text(
            text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=markup
        )

    def send_change_refresh_interval(self):

        self.editing_prop = "refresh_interval"
        interval = self.processor.get_refresh_interval(self.group_id)
        if not interval:
            self.send_group_not_found()
            return
        button = telegram.InlineKeyboardButton(text=Label.BACK, callback_data="selPrp")
        markup = telegram.InlineKeyboardMarkup.from_button(button)
        text = Message.SETTING_REFRESH_INTERVAL.format(
            TITLE=self.group_title, INTERVAL=interval
        )
        self.base_message.edit_text(
            text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=markup
        )

    def send_delete(self):

        text = Message.DELETE_GROUP.format(TITLE=self.group_title)
        buttons = [
            telegram.InlineKeyboardButton(
                text=Label.DELETE_CONFIRM, callback_data="delCfm"
            ),
            telegram.InlineKeyboardButton(text=Label.BACK, callback_data="selPrp"),
        ]
        markup = telegram.InlineKeyboardMarkup.from_row(buttons)
        self.base_message.edit_text(
            text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=markup,
        )

    def send_group_not_found(self):

        self.groups = self.processor.get_controlled_groups(self.user.id)
        text = Message.GROUP_NOT_FOUND.format(TITLE=self.group_title)
        self.base_message.edit_text(text=text, parse_mode=telegram.ParseMode.HTML)
        self.send_select_group()

    def send_select_group(self, edit=True):

        if edit:
            sender = self.base_message.edit_text
        else:
            sender = self.chat.send_message

        if not self.groups:
            msg = sender(
                text=Message.NO_COMMON_GROUPS, parse_mode=telegram.ParseMode.HTML
            )

        else:
            buttons = [
                telegram.InlineKeyboardButton(text=title, callback_data=f"grp={id}")
                for id, title in self.groups.items()
            ]
            markup = telegram.InlineKeyboardMarkup.from_column(buttons)
            msg = sender(
                text=Message.SETTINGS_SELECT_GROUP,
                parse_mode=telegram.ParseMode.HTML,
                reply_markup=markup,
            )

        self.base_message = msg

    def send_select_property(self, edit=True):

        if edit:
            sender = self.base_message.edit_text
        else:
            sender = self.chat.send_message

        text = Message.SETTINGS_SELECT_PROPERTY.format(TITLE=self.group_title)
        buttons = [
            [
                telegram.InlineKeyboardButton(
                    text=Label.CLEAN_INTERVAL, callback_data="clnInt"
                ),
                telegram.InlineKeyboardButton(text=Label.PROMPT, callback_data="prt"),
            ],
            [
                telegram.InlineKeyboardButton(
                    text=Label.REFRESH_INTERVAL, callback_data="refInt"
                ),
                telegram.InlineKeyboardButton(text=Label.UPDATE, callback_data="upd"),
            ],
            [
                telegram.InlineKeyboardButton(
                    text=Label.DELETE_GROUP, callback_data="delGrp"
                )
            ],
            [telegram.InlineKeyboardButton(text=Label.BACK, callback_data="selGrp")],
        ]
        markup = telegram.InlineKeyboardMarkup(buttons)

        msg = sender(text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=markup)
        self.base_message = msg

    def send_update_data(self):

        chat_ids = self.processor.get_chat_ids(self.group_id)
        old_title = self.group_title
        new_title = get_chat_title(chat_ids[-1], self.bot)
        old_admins = self.processor.get_admins(self.group_id)
        new_admins = get_admins(chat_ids, self.bot)

        self.processor.set_title(self.group_id, new_title)
        self.processor.set_admins(self.group_id, new_admins)
        self.group_title = self.groups[self.group_id] = new_title

        text = Message.SETTING_UPDATE.format(
            TITLE=new_title,
            OLD_TITLE=old_title,
            NEW_TITLE=new_title,
            OLD_COUNT=len(old_admins),
            NEW_COUNT=len(new_admins),
        )
        button = telegram.InlineKeyboardButton(text=Label.BACK, callback_data="selPrp")
        markup = telegram.InlineKeyboardMarkup.from_button(button)
        self.base_message.edit_text(
            text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=markup
        )
