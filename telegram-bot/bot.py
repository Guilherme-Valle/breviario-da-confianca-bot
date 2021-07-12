from telegram.ext import Updater, CommandHandler
import telegram
from datetime import date, timedelta
import locale
import os
import json
from utils import *

def get_meditation_from_website(selected_date):
    # Deleta arquivo de output prévio
    os.system('rm -f ~/breviario-da-confianca-bot/crawler/crawler/spiders/output.json || true')

    # Script para rodar o webcrawling, passando como parâmetro a data
    script = 'cd ~/breviario-da-confianca-bot/crawler/crawler/spiders && /usr/local/bin/scrapy crawl breviario_spider -a selected_date=' \
             + str(selected_date.day) + '/' + str(selected_date.month) + ' -o output.json'
    os.system(script)

    # Processa o arquivo de output gerado pelo crawler, extraindo dele o texto da meditação
    with open(r'/root/breviario-da-confianca-bot/crawler/crawler/spiders/output.json') as json_file:
        meditation = json.load(json_file)

    return "<b>" + meditation[0]['meditation_day'] + " - " + meditation[0]['title'] + " </b> \n \n" + meditation[0]['text'] \
                      + "\n \n <i>" + meditation[0]['reference'] + "</i>"



def get_today_meditation(update, context):
    chat_id = update.message.chat_id
    today = date.today()
    print(today)

    text_meditation = get_meditation_from_website(today)

    context.bot.send_message(chat_id=chat_id, text=text_meditation, parse_mode=telegram.ParseMode.HTML)



def get_tomorrow_meditation(update, context):
    chat_id = update.message.chat_id
    tomorrow = date.today() + timedelta(days=1)
    print(tomorrow)

    text_meditation = get_meditation_from_website(tomorrow)

    context.bot.send_message(chat_id=chat_id, text=text_meditation, parse_mode=telegram.ParseMode.HTML)


def print_date_invalid_error(chat_id, context):
    context.bot.send_message(chat_id=chat_id,
                             text='Por favor, digite uma data <b>válida</b> no formato <b>DD/MM</b>.',
                             parse_mode=telegram.ParseMode.HTML)

def get_custom_meditation(update, context):
    chat_id = update.message.chat_id

    if len(context.args) == 0:
        print_date_invalid_error(chat_id, context)
        return

    selected_date = context.args[0]

    if string_has_letter(selected_date) or not string_has_bar(selected_date):
        print_date_invalid_error(chat_id, context)
        return

    selected_day, selected_month, *rest = [int(x) for x in selected_date.split('/')]

    if (selected_day <= 0 or selected_day > 31 or (selected_month == 2 and selected_day > 29) or selected_month <= 0
    or selected_month > 12):
        print_date_invalid_error(chat_id, context)
        return

    selected_date = date(2020, selected_month, selected_day)
    text_meditation = get_meditation_from_website(selected_date)

    context.bot.send_message(chat_id=chat_id, text=text_meditation, parse_mode=telegram.ParseMode.HTML)


def main():
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    key_api = os.environ.get('PYTHON_API_BREVIARIO_KEY')

    updater = Updater(key_api, use_context=True)
    dispatcher = updater.dispatcher

    # Métodos do bot
    dispatcher.add_handler(CommandHandler('meditacaodehoje', get_today_meditation))
    dispatcher.add_handler(CommandHandler('meditacaodeamanha', get_tomorrow_meditation))
    dispatcher.add_handler(CommandHandler('meditacao', get_custom_meditation, pass_args=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()