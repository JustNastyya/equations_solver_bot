import telebot
from config import *
from mainFunctions import *

bot = telebot.TeleBot(token)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)  # main keyboard with 4 buttons
keyboard1.row('проверить знание', 'познать таинство', 'ничего не понял', 'нашел ошибку')


def main(message):
    summ = message
    if summ != 'check ':
        summ = summ[summ.index('k') + 1:]

        while ' ' in summ:  # delete spaces
            smth = summ.index(' ')
            summ = summ[0:smth]+summ[smth+1:len(summ)]
        if summ == '' or summ[0] == '=':  # preparing a string
            mistake = True 
        if not('=0' in summ):
            summ += '=0'

        mistake, coeff, unknown = stringToList(summ)

        if mistake or coeff[-1] == 0:
            return 'Вы неправильно ввели уравнение'

        # the main part
        table, korni, coeff_line, divs = resutCalc(coeff)

        # output part
        output = ''
        for i in range(len(korni)):  # usual answers to x
            if korni[i] > 0:
                output = output + '(' + unknown + str(-korni[i]) +  ')'
            else:
                output = output + '('+ unknown + '+' + str(-korni[i]) + ')'

        if table[len(table) - 1][len(table[len(table) - 1]) - 1] != 0 and korni == []:
            return 'Нет решения через схему Горнера'  # if Discriminant havent got square root

        elif (len(table[0]) >= 4):
            output += '('
            for i in range(1, len(table[0])):
                if table[coeff_line][i] > 0:
                    output += '+'
                if i == len(table[0]) - 1:
                    output += str(table[coeff_line][i]) + ')'
                elif i == len(table[0]) - 2:
                    output += str(table[coeff_line][i]) + unknown
                else:
                    output += str(table[coeff_line][i]) + unknown + '^' + str(len(table[0]) - i - 1)

        else: # last number 
            if table[divs][2] > 0:
                output = output + '(' + unknown + '+' + str(table[divs][2]) +  ')'
            else:
                output = output + '('+ unknown + str(table[divs][2]) + ')'

        if output != '':
            output = output + '=0'
            return output


'''                     ______main part______                   '''

@bot.message_handler(commands = ['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую, я помогу тебе познать таинство схемы Горнера. Хочешь ли ты получить бесценные знания или проверить свои?', reply_markup = keyboard1)


@bot.message_handler(content_types = ['text'])
def send_text(message):  # if users message is a text
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, брооо')

    elif message.text.lower() == 'проверить знание':
        bot.send_message(message.chat.id, 'Отлично, напиши "check",\
        а после твое уравнение вида "ax^n..+bx^2+cx+d=0" и жди магию')

    elif message.text.lower() == 'ничего не понял':
        bot.send_message(message.chat.id, 'Вообщем нужно взять уравнение\
            которое физический можно решить по схеме Горнера и написать \
            мне его после "check", дальше будет интересно')

    elif message.text.lower() == 'нашел ошибку':
        bot.send_message(message.chat.id, 'Ну чтож, видимо я не идеален ..\
            раз уж ты тут - сообщи об ошибке моему создателю, @JustNastyaa, спасибо')

    elif message.text.lower() == 'познать таинство':
        bot.send_message(message.chat.id, theoryText)

    elif message.text.lower() == 'я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')

    elif 'check' in message.text.lower():
        ms = message.text.lower()
        bot.send_message(message.chat.id, main(ms))
    else:
        bot.send_message(message.chat.id, 'Таких иероглифов нет в моих писаньях')


bot.polling(none_stop=True)