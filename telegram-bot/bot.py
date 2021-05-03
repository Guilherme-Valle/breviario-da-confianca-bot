from telegram.ext import Updater, CommandHandler
from datetime import date
import locale


def get_today_meditation():
    today = date.today()
    str(today.day) + '/' + str(today.month)
    return 1


def main():
    locale.setlocale(locale.LC_TIME, "pt_BR")
    updater = Updater('token')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('MeditacaoDeHoje', get_today_meditation))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()