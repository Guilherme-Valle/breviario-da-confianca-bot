from telegram.ext import Updater, CommandHandler
from datetime import date
import locale


def get_today_meditation(bot, update):
    chat_id = update.message.chat_id
    today = date.today()
    bot.send_message(chat_id=chat_id, text=str(today.day) + '/' + str(today.month))


def main():
    locale.setlocale(locale.LC_TIME, "pt_BR")
    updater = Updater('token')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('MeditacaoDeHoje', get_today_meditation))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()