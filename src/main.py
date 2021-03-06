import telebot
import random
import re


with open('./secrets/token.txt', 'r') as f:
    token = f.readline()
    bot = telebot.TeleBot(token)
    is_random = False
    is_choice = False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, f'Hello, {message.from_user.first_name}!')


@bot.message_handler(commands=['random'])
def send_welcome(message):
    global is_random
    global is_choice
    
    if is_choice:
        is_choice = False
     
    is_random = True
    bot.send_message(message.from_user.id, 'Input max number:')


@bot.message_handler(commands=['choice'])
def send_welcome(message):
    global is_random
    global is_choice
    
    if is_random:
        is_random = False

    is_choice = True
    bot.send_message(message.from_user.id, 'Input options (separated by spaces):')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global is_random
    global is_choice

    if is_random:
        try:
            max_num = int(message.text)
            if max_num > 0:
                rand_num = random.randint(0, max_num)
                bot.send_message(message.from_user.id, 'Your random number is ' + str(rand_num))
            else:
                bot.send_message(message.from_user.id, 'Not a correct number!')
        except ValueError:
            bot.send_message(message.from_user.id, 'Not a correct number!')
        
        is_random = False
    elif is_choice:
        options = re.split(' +', message.text)
        choice = random.choice(options)
        bot.send_message(message.from_user.id, 'Your choice is ' + choice)

        is_choice = False
    else:
        bot.send_message(message.from_user.id, 'Sorry, I don\'t understand...')


if __name__ == '__main__':
    bot.polling(none_stop=True)