#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from collections import defaultdict
from uuid import uuid4

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

UserCounter = 0

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!\n/add <time in format hh:mm> <name of your event>\n/check to look at your events\n/erase <time> to erase your event from the list')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    #update.message.reply_text(update.message.text)
    update.message.reply_text("I don't know what does it mean! Write /help to see the command list")

def def_value():
    return ""

#event = defaultdict(def_value)

def check_digits(t):
    digs = '1234567890'
    if t[0] in digs and t[1] in digs and t[3] in digs and t[4] in digs:
        return 1
    return 0

def add_command(update: Update, context: CallbackContext) -> None:
    user_asks = context.args
    if len(user_asks) < 2:
        update.message.reply_text('Incorrect')
        return
    t = user_asks[0]
    if len(t) != 5 or t[2] != ':' or not check_digits(t) or int(t[0:2]) > 23 or int(t[3:5]) >= 60:
        update.message.reply_text('Incorrect')
        return
    #context.user_data.update({user_asks[0] : context.user_data[user_asks[0]] + ' '.join(user_asks[1:]) + '; '})
    context.user_data[user_asks[0]] = context.user_data.get(user_asks[0], '') + ' '.join(user_asks[1:]) + '; '
    update.message.reply_text('New event')

def check_events(update: Update, context: CallbackContext) -> None:
    if len(context.user_data) == 0:
        update.message.reply_text('Empty')
        return
    s = str('')
    for x in context.user_data:
        s += x + ': ' + context.user_data[x] + '\n'
    update.message.reply_text(s)


def erase_command(update: Update, context: CallbackContext) -> None:
    user_asks = context.args
    if len(user_asks) > 1:
        update.message.reply_text('incorrect')
        return
    if user_asks[0] not in context.user_data:
        update.message.reply_text('incorrect')
        return
    context.user_data.pop(user_asks[0])
    update.message.reply_text('Event removed')

#def get_myid(update: Update, context: CallbackContext) -> None:
#    update.message.reply_text(str(uuid4()))

'''def clear_command(update: Update, context: CallbackContext) -> None:
    context.user_data = dict()
    return
'''
def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5070779317:AAE5wEOALXDry77503tJk0xlaskYvXAiwok")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("add", add_command))
    dispatcher.add_handler(CommandHandler("check", check_events))
    dispatcher.add_handler(CommandHandler("erase", erase_command))
    '''dispatcher.add_handler(CommandHandler("clear", clear_command))'''
    #dispatcher.add_handler(CommandHandler("myid", get_myid))
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()