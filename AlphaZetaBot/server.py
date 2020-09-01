import logging
import telegram.ext

from .functions import get_configuration, refresh_invite_link
from .processor import Processor
from .handles import handles

config = get_configuration()


class Server:
    def __init__(self):

        self.logger = logging.getLogger()
        self.updater = telegram.ext.Updater(
            token=config["TOKEN"], user_sig_handler=self.sig_handler
        )

        self.updater["ADMINS"] = config["ADMINS"]
        self.updater["CLEAN_INTERVAL"] = config["CLEAN_INTERVAL"]
        self.updater["GATEWAY"] = config["GATEWAY"]
        self.updater["GROUP"] = config["GROUP"]
        self.updater["INVITE_LINK"] = config["INVITE_LINK"]
        self.updater["MODERATE"] = config["MODERATE"]
        self.updater["START_LINK"] = config["START_LINK"]

        self.updater.job_queue.run_repeating(
            callback=refresh_invite_link, interval=config["REFRESH_INTERVAL"], first=0
        )

        self.processor = Processor(config["DATABASE_URL"])
        self.setup_handles()

    def poll(self):

        self.updater.start_polling()
        self.updater.idle()

    def run(self):

        self.updater.start_webhook(
            listen="0.0.0.0", port=config["PORT"], url_path=config["TOKEN"]
        )
        self.updater.bot.set_webhook(url=config["URL"])
        self.updater.start_webhook()
        self.updater.idle()

    def setup_handles(self):

        dispatcher = self.updater.dispatcher
        for handler, args_lx in handles.items():
            for args_h, args_d in args_lx:
                handle = handler(*args_h)
                dispatcher.add_handler(handle, *args_d)

    def sig_handler(self, *args):

        self.logger.info(f"Got Signal : {args}")
        self.processor.close()
