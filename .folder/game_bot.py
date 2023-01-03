# Условие игры: На столе лежит 117 конфета. Играют два игрока делая ход друг после друга. 
# Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем 28 конфет. 
# Все конфеты оппонента достаются сделавшему последний ход.

import telebot
from random import randint
from random import choice

bot = telebot.TeleBot("5924736461:AAHyjUG9LH3WdWrY9SIPRAxScaXYx4GsqQE")
sweets = dict()
start_game = dict()
player = dict()


def handle_game_proc(message):
    global start_game
    try:
        if start_game[message.chat.id] and 1 <= int(message.text) <= 28:
            return True
        else:
            return False
    except KeyError:
        start_game[message.chat.id] = False
        if start_game[message.chat.id] and 1 <= int(message.text) <= 28:
            return True
        else:
            return False


@bot.message_handler(commands=['game'])
def send_welcome(message):
    global player, sweets, start_game
    bot.reply_to(message, "Let's go")
    sweets[message.chat.id] = 117
    player[message.chat.id] = choice(['Bot', 'User'])
    bot.send_message(message.chat.id, f'Начинает {player[message.chat.id]}')
    start_game[message.chat.id] = True
    if player[message.chat.id] == 'Bot':
        take = randint(1, sweets[message.chat.id] % 28)
        sweets[message.chat.id] -= take
        bot.send_message(message.chat.id, f'Бот взял {take}')
        bot.send_message(message.chat.id,
                         f'Осталось {sweets[message.chat.id]}')
        player[message.chat.id] = 'User'


@bot.message_handler(func=handle_game_proc)
def game_process(message):
    global sweets, player, start_game
    if player[message.chat.id] == 'User':
        if sweets[message.chat.id] > 28:
            sweets[message.chat.id] -= int(message.text)
            bot.send_message(message.chat.id,
                             f'Осталось {sweets[message.chat.id]}')
            if sweets[message.chat.id] > 28:
                take = randint(1, sweets[message.chat.id] % 28)
                sweets[message.chat.id] -= take
                bot.send_message(message.chat.id,
                                 f'Бот взял {take}')
                bot.send_message(message.chat.id,
                                 f'Осталось {sweets[message.chat.id]}')
                if sweets[message.chat.id] <= 28:
                    bot.send_message(message.chat.id, 'User Win')
                    start_game[message.chat.id] = False
            else:
                bot.send_message(message.chat.id, 'Bot Win')
                start_game[message.chat.id] = False
        else:
            bot.send_message(message.chat.id, 'Bot Win')
            start_game[message.chat.id] = False


bot.infinity_polling()

