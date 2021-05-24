#import statements
import logging
import getgecko
import time
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters


#to create logs
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


#telegram bot access token
token = '1884755931:AAG3bkd_6zW_G9KDwtK19emR3ejvvDKdpVU'

bot = telegram.Bot(token)


#setting updater and dispatcher
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


#bot_commands
bot_commands = '1. /cryptoprice'


#to respond to /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm techlabot. Your bot, your tech!\nTo see a list of commands enter '/Commands'")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# #to list commands to user
# def commands(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text='Enter any of the following commands\n' + bot_commands)
# commands_handler = CommandHandler('commands', commands)
# dispatcher.add_handler(commands_handler)


# #to list crypto details to user
# def cryptoprice(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text='Enter the coin name and currency pair\nExample1 : bitcoin usd\nExample2 : ethereum eur')
#     context.bot.send_message(chat_id=update.effective_chat.id, text=getgecko.displaycryptoprice())
# crypto_handler = CommandHandler('cryptoprice', cryptoprice)
# dispatcher.add_handler(crypto_handler)
    

#to return unknown status
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I did not understand that command. Please try again.")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


#to give user alert
def user_input(update, context):
    user_input = update.message.text

    if (user_input.startswith('price')):
        pricelist = user_input.split()
        if (len(pricelist)==3):
            coin = pricelist[1].lower()
            currencypair = pricelist[2].lower()
            update.message.reply_text("The price of " + coin + " is " + getgecko.displaycryptoprice(coin, currencypair) + " " + currencypair.upper())
        else:
            update.message.reply_text("Please enter the correct format")

    if (user_input.startswith('alert')):
        alertlist = user_input.split()
        if (len(alertlist)==5):
            print(alertlist)
            coin = alertlist[1].lower()
            currencypair = alertlist[4].lower()
            compare = alertlist[2].lower()
            targetprice = float(alertlist[3])
            currentprice = getgecko.displaycryptoprice(coin, currencypair)
            update.message.reply_text("Alert for " + coin + " at price " + str(targetprice) + " is set")
            stop = True
            if (compare=="gte"):
                while stop==True:
                    if(float(currentprice)>=targetprice):
                        update.message.reply_text("Alert triggered\nCurrent price of " + coin + " is " + getgecko.displaycryptoprice(coin, currencypair) + " " + currencypair.upper())
                        stop = False
                    else:
                        time.sleep(10)
                        currentprice = getgecko.displaycryptoprice(coin, currencypair)
            elif (compare=="lte"):
                print("in lte")
                while stop==True:
                    print("in while")
                    if(float(currentprice)<=targetprice):
                        print("in if")
                        update.message.reply_text("Alert triggered\nCurrent price of " + coin + " is " + getgecko.displaycryptoprice(coin, currencypair) + " " + currencypair.upper())
                        stop = False
                    else:
                        time.sleep(10)
                        currentprice = getgecko.displaycryptoprice(coin, currencypair)
            else:
                update.message.reply_text("Invalid comparison. Please try again")
        else:
            update.message.reply_text("Please enter the correct format\nExample: alert bitcoin GTE 50000 usd")

    if (user_input=="techlabotterminate"):
        update.message.reply_text("Techlabot is shut down")
        updater.stop()

text_handler = MessageHandler(Filters.text, user_input)
dispatcher.add_handler(text_handler)    


#starting the bot
updater.start_polling()


#to stop execution until a signal is received
updater.idle()
