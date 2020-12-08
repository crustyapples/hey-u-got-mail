from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging

updater = Updater(token='1497277546:AAF00RNk8Fr8dGjfBQhbyAY17Cayz9rcY10', use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

def inline_functions(update, context):
    query = update.inline_query.query
    caps_option = InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    greentea_option = InlineQueryResultArticle(
        id=query,
        title='GREEN TEA',
        input_message_content=InputTextMessageContent("i like ayataka only pls")
    )
    
    with open("orders.txt", "r") as c:
        orders = c.read()

    card_orders = InlineQueryResultArticle(
        id= f"order {query}",
        title='TOTAL ORDERS',
        input_message_content=InputTextMessageContent(orders)
    )

    if not query:
        return

    results = [caps_option, greentea_option, card_orders]
    context.bot.answer_inline_query(update.inline_query.id, results)

inline_caps_handler = InlineQueryHandler(inline_functions)
dispatcher.add_handler(inline_caps_handler)

updater.start_polling()