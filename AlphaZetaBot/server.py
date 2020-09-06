from os import getenv
import logging
import telegram.ext

from .functions import periodic_job
from .processor import Processor
from .handles import handles


class Server:
    def __init__(self):

        self.processor = Processor(getenv("DATABASE_URL"))
        self.updater = telegram.ext.Updater(
            token=getenv("TOKEN"), use_context=True, user_sig_handler=self.sig_handler
        )

        bot_data = self.updater.dispatcher.bot_data
        intervals = self.processor.get_intervals()
        intervals_ = [
            (id, cln_int, 1, ref_int, 1) for (id, cln_int, ref_int) in intervals
        ]

        bot_data["intervals"] = intervals_
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

    def sig_handler(self, *args):

        logging.info("Got Signal : %s", args)
        self.processor.close()
