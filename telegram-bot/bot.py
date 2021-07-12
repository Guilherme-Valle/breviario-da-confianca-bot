from telegram.ext import Updater, CommandHandler
import telegram
from datetime import date, timedelta
import locale
import os
import json

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

    text_meditation = get_meditation_from_website(today)

    context.bot.send_message(chat_id=chat_id, text=text_meditation, parse_mode=telegram.ParseMode.HTML)



def get_tomorrow_meditation(update, context):
    chat_id = update.message.chat_id
    tomorrow = date.today() + timedelta(days=1)

    text_meditation = get_meditation_from_website(tomorrow)

    context.bot.send_message(chat_id=chat_id, text=text_meditation, parse_mode=telegram.ParseMode.HTML)



def main():
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    key_api = os.environ.get('PYTHON_API_BREVIARIO_KEY')

    updater = Updater(key_api, use_context=True)
    dispatcher = updater.dispatcher

    # Métodos do bot
    dispatcher.add_handler(CommandHandler('meditacaodehoje', get_today_meditation))
    dispatcher.add_handler(CommandHandler('meditacaodeamanha', get_tomorrow_meditation))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()