# Данные взяты из описания ePay
# https://epayment.kz/docs/platezhnaya-stranica

import json
import logging
import configparser
import requests

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Configure Bot
config = configparser.ConfigParser()
config.read("config.ini")
bot_token = config["main_settings"]["token"]

# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens the web app."""
    await update.message.reply_text(
        "Нажмите кнопку внизу чтобы попробовать оплатить (ТЕСТ)",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Оплатить",
                web_app=WebAppInfo(url="https://tarelkasemok.github.io/tg-web-app-bot/kkb_pay.html"),
            )
        ),
    )


# # Handle incoming WebAppData
# async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Print the received data and remove the button."""
#     # Here we use `json.loads`, since the WebApp sends the data JSON serialized string
#     # (see webappbot.html)
#     data = json.loads(update.effective_message.web_app_data.data)
#     await update.message.reply_html(
#         text=f"You selected the color with the HEX value <code>{data['hex']}</code>. The "
#         f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>.",
#         reply_markup=ReplyKeyboardRemove(),
#     )

def kkb_get_auth_token():
    url = "https://testoauth.homebank.kz/epay2/oauth2/token"
    req_body = {
            "grant_type":       "client_credentials",
            "scope": 			"payment",
            "client_id": 		"test",
            "client_secret": 	"yF587AV9Ms94qN2QShFzVR3vFnWkhjbAK3sG",
            "invoiceID": 		"005681201",
            "amount": 		    100,
            "curency": 		    "KZT",
            "terminal": 		"67e34d63-102f-4bd1-898e-370781d0074d",
            "postLink":         "",
            "failurePostLink":  ""
    }
    req = requests.post(url, data=req_body)
    print(req.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    # application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()