from os import getenv
import logging
import telegram.ext

from .functions import get_intervals, periodic_job
from .processor import Processor
from .handles import handles


class Server:
    def __init__(self):

        self.processor = Processor(getenv("DATABASE_URL"))
        self.updater = telegram.ext.Updater(
            token=getenv("TOKEN"), use_context=True, user_sig_handler=self.sig_handler
        )

        bot_data = self.updater.dispatcher.bot_data
        bot_data["ALLOW_CREATE"] = getenv("ALLOW_CREATE", "True").lower() == "true"
        bot_data["cache"] = {}
        bot_data["intervals"] = get_intervals(self.processor)
        bot_data["processor"] = self.processor

        self.updater.job_queue.run_repeating(
            callback=periodic_job, interval=60, first=0
        )
        self.setup_handles()

    def listen(self):

        logging.info("Started listening")
        self.updater.start_webhook(
            listen="0.0.0.0", port=getenv("PORT"), url_path=getenv("TOKEN")
        )
        self.updater.bot.set_webhook(url=getenv("URL"))
        self.updater.start_webhook()
        self.updater.idle()

    def poll(self):

        logging.info("Started polling")
        self.updater.start_polling()
        self.updater.idle()

    def setup_handles(self):

        dispatcher = self.updater.dispatcher
        for handler, args_lx in handles.items():
            for args_h, args_d in args_lx:
                handle = handler(*args_h)
                dispatcher.add_handler(handle, *args_d)
        # dispatcher.add_error_handler(lambda _, ctx: logging.error(ctx.error))

    def sig_handler(self, *args):

        logging.info("Got Signal : %s", args)
        self.processor.close()
