import psycopg2
import time

import telegram.ext
from telegram import *
from telegram.ext import *

TOKEN = '5001833868:AAF3h5D-4dGZ81uXdQF_zu1BtsApwRRBHKk'


def start(update, context):
    firstname = update.message.from_user.first_name
    update.message.reply_text(
        f'Hi {firstname}, I\'m a robot named pkob_269509_bot, please click the button below to start the program to '
        f'help solve your problem. ',
        reply_markup=start_keyboard())


def main_menu(update, context):
    update.callback_query.message.reply_text(
        f'Please click the button below to continue using the robot.',
        reply_markup=main_keyboard())


def check_details(update, context):
    update.callback_query.message.reply_text(
        'Please insert ic number and phone number to check the details. For example: "990101095201@0123456789"')


def website(update, context):
    update.callback_query.message.reply_text(
        'Website Link: https://pkob269509.herokuapp.com/')
    update.callback_query.message.reply_text(
        f'Please click the button below to continue using the robot.',
        reply_markup=main_keyboard())


def about(update, context):
    update.callback_query.message.reply_text(
        'Hi, what do you want to know about this system?',
        reply_markup=about_keyboard())


def about_developer(update, context):
    update.callback_query.message.reply_text(
        'Developer\'s Link: https://github.com/jiaearn')
    update.callback_query.message.reply_text(
        f'Please click the button below to continue using the robot.',
        reply_markup=main_keyboard())


def about_bot(update, context):
    update.callback_query.message.reply_text(
        f'This is a robot used for real-time programming assignment 2 purpose.'
        f'This robot has multiple functions: \n\n'
        f'1. We can read data from database from Heroku server that has been developed for Assignment-1.\n'
        f'2. We can go directly to the website that has been developed for Assignment-1. \n'
        f'3. We can go directly to the developer\'s GitHub website. \n')
    update.callback_query.message.reply_text(
        f'Please click the button below to continue using the robot.',
        reply_markup=main_keyboard())


def handle_message(update, context):
    text = str(update.message.text).lower()
    if '@' in text:
        message = victim_details(text)
        update.message.reply_text(message)
        update.message.reply_text(
            f'Please click the button below to continue using the robot.',
            reply_markup=main_keyboard())
    elif "hi" in text or "hey" in text or "hello" in text:
        message = 'Hi, I\'m a robot named pkob_269509_bot, please click the button below to start the program to help ' \
                  'solve your problem. '
        update.message.reply_text(message, reply_markup=main_keyboard())
    else:
        message = 'Hi, I\'m a robot named pkob_269509_bot, please click the button below to start the program to help ' \
                  'solve your problem. '
        update.message.reply_text(f"You said {update.message.text}. Sorry i don't understand this command.")
        update.message.reply_text(message, reply_markup=main_keyboard())


def start_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Start now', callback_data='start'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Check', callback_data='main1'),
            InlineKeyboardButton('Website', callback_data='main2'),
            InlineKeyboardButton('About', callback_data='main3')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def about_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('About developer', callback_data='about1'),
            InlineKeyboardButton('About bot', callback_data='about2'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def victim_details(message):
    ic_no = message.split("@")[0]
    phone = message.split("@")[1]
    try:
        con = psycopg2.connect(
            "postgres://qplearpjyxzbwu:1ae1203a8acfb2a093a156d254dcdaae3681165a2d0cedbd31541985f66c49bd@ec2-52-20-194-52.compute-1.amazonaws.com:5432/dcfn4v8ku99eb3")
        cur = con.cursor()
        cur.execute(f"SELECT ic_no,name,phone FROM \"App_Victim_victim\" WHERE ic_no = '{ic_no}' AND phone = '{phone}'")
        result = cur.fetchall()

        ic = [i[0] for i in result]
        phone = [i[1] for i in result]
        name = [i[2] for i in result]
        age = str(age_count(str(ic[0])))

        results = "Kad Pengenalan: " + str(ic[0]) + "\nNombor Telefon: " + str(phone[0]) + "\nNama: " + str(
            name[0]) + "\nUmur: " + age
        cur.close()
    except (Exception, psycopg2.DatabaseError):
        results = "Sorry, data is not in list. Please try again."

    return results


def age_count(ic_no):
    ic_year = int(ic_no[0:2])
    cur_year = int(time.strftime("%y", time.localtime()))
    if ic_year > cur_year:
        age = cur_year - ic_year + 100
    else:
        age = cur_year - ic_year
    return age


updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(CommandHandler('start', start))
disp.add_handler(CallbackQueryHandler(main_menu, pattern='start'))
disp.add_handler(CallbackQueryHandler(main_menu, pattern='back'))
disp.add_handler(CallbackQueryHandler(check_details, pattern='main1'))
disp.add_handler(CallbackQueryHandler(website, pattern='main2'))
disp.add_handler(CallbackQueryHandler(about, pattern='main3'))
disp.add_handler(CallbackQueryHandler(about_developer, pattern='about1'))
disp.add_handler(CallbackQueryHandler(about_bot, pattern='about2'))
disp.add_handler(MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_polling()
updater.idle()
