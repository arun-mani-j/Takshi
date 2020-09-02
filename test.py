import telegram.ext

TOKEN = "1279417229:AAEaKMvHI-rgRlhrG9zwSPWrzOVjn3sDJFs"

def say_hello(ctx):

    print("Got a good context")

updater = telegram.ext.Updater(token=TOKEN, use_context=True, user_sig_handler=print)
updater.job_queue.run_repeating(say_hello, interval=60, first=0)
updater.dispatcher.add_handler(telegram.ext.CommandHandler("start", print))
updater.start_polling()
updater.idle()
