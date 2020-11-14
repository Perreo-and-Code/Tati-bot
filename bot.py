import logging
import os
import sys
import telegram
from telegram.ext import Updater, CommandHandler
import random
from jira.sprint_daily import dataSprint

# config logggin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()

# solicitar token

TOKEN = os.getenv("TOKEN")

mode = os.getenv("MODE")
if mode == "dev":
    # Acceso local
    def run(updater):
        updater.start_polling()
        print("Bot cargado")
        updater.idle()  # permite finalizar nuestro bot con ctrl + c
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook(
            f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
else:
    logger.info("No se especifico el MODE.")
    sys.exit(1)


def greet(update, context):
    logger.info(f"El usuario {update.effective_user['username']}, ha saludado")
    name = update.effective_user['first_name']
    greets = ['Hello', 'Welcome', 'Greetings!',
              'Salutatons!', 'Good day!', 'Yo!']
    update.message.reply_text(f"{random.choice(greets)}, {name}")


def sprintDaily(update, context):
    """ Get data from api Jira sprint """
    chat = update.effective_chat['id']
    username = update.effective_user['username']

    logger.info(f"The User {username}, has get information about sprint")

    message = dataSprint()

    context.bot.sendMessage(
        chat_id=chat,
        parse_mode='HTML',
        text=message)


if __name__ == "__main__":
    # obtenemos informacion de nuestro bot
    my_bot = telegram.Bot(token=TOKEN)

    # enlazamos updater con nuestro bot
    updater = Updater(my_bot.token, use_context=True)

    # creamos despachador
    dp = updater.dispatcher

    # creamos manejador
    dp.add_handler(CommandHandler("hi", greet))
    dp.add_handler(CommandHandler('sprintDaily', sprintDaily))

    run(updater)
