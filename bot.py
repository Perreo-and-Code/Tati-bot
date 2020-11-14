import logging
import os
import sys
import telegram
from telegram.ext import Updater, CommandHandler
import random
from functions.scrapper import getTeslaActionsPrice

# config logggin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()

# request token
TOKEN = os.getenv("TOKEN")
# request mode
mode = os.getenv("MODE")
if mode == "dev":
    # Acceso local
    def run(updater):
        updater.start_polling()
        print("Bot Ready")
        updater.idle()  # permite finalizar nuestro bot con ctrl + c
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook(
            f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
else:
    logger.info("Specify MODE..")
    sys.exit(1)


def greet(update, context):
    """Function that show random greet"""
    name = update.effective_user['first_name']
    greets = ['Hello', 'Welcome', 'Greetings!',
              'Salutatons!', 'Good day!', 'Yo!']
    update.message.reply_text(f"{random.choice(greets)}, {name}")


def tesla(update, context):
    """call getTeslaActionsPrice and show the value of this"""
    update.message.reply_text(
        f"tesla actions price: ${getTeslaActionsPrice()} USD")


if __name__ == "__main__":
    # get information from the bot
    my_bot = telegram.Bot(token=TOKEN)

    # link updater with the bot
    updater = Updater(my_bot.token, use_context=True)

    # create dispatcher
    dp = updater.dispatcher

    # create handler
    dp.add_handler(CommandHandler("hi", greet))
    dp.add_handler(CommandHandler("tesla", tesla))

    run(updater)
