import telebot
# from config import *
# from mainFunctions import *
token = '699538373:AAFerfMwSTYbcBA0gDY0tiUoSrumlVSYoY8'

bot = telebot.TeleBot(token)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)  # main keyboard with 4 buttons
keyboard1.row('проверить знание', 'познать таинство', 'ничего не понял', 'нашел ошибку')


token = '699538373:AAFerfMwSTYbcBA0gDY0tiUoSrumlVSYoY8'

theoryText = '''
    Принцип работы этой схемы намного проще показать на примере.
Допустим у нас есть уравнение: x^3 – x^2 – 8x + 12 = 0. 
Для начала мы находим все делители свободного члена,
в нашем случае свободный член это 12, а его делители это
        +-1, +-2, +-3, +-4, +-6, +-12.
    Далее мы должны взять все коэффициенты при x и занести их
в таблицу по горизонтали, а делители свободного члена занести
по очереди по вертикали. 
            |   1| -1| -8| 12
          1|   1|  0| -8| 4
         -1|     |     |    |
        ...  |     |     |    |
    После мы проделываем одну и ту же операцию, заполняя
ячейки. Единицу в первую ячейку мы всегда сносим, а чтобы
заполнить вторую нам надо умножить предыдущую ячейку на
делитель этой строчки и сложить с коэффициентом данного
столбца. То есть чтобы заполнить вторую ячейку: 1*1 + (-1).
Мы получаем 0, и проделываем ту же операцию для следующей
ячейки: 0*1 +(-8), получая -8. Аналогично для третьей
ячейки мы получаем 4. Теперь таблица выглядит так:
           |   1| -1| -8| 12
         1|   1|  0| -8| 4
        -1|     |    |     |
        ... |     |    |     |
    В последней ячейке мы получили 4, значит, 1 не является
корнем. Мы проделываем ту же операцию с остальными
делителями, пока в конце не получится 0, что будет значить,
что этот делитель – корень.
         |  1| -1|-8|12
        1|  1|  0|-8|4
       -1|  1| -2| 6|6
        2|   1|  1|-6|0
       ...|     |    |    |
    Мы нашли первый корень – 2, теперь уравнение выглядит так: 
        (x^2 + x – 6) (x – 2) = 0.
    Чтобы получить такое уравнение мы разделили
x^3 – x^2 – 8x + 12 = 0 на (x – 2), но это можно не делать,
ведь все нужные коэффициенты мы уже получили, они находятся в ряду, в котором мы получили 0. 
        2   |1   |1   |-6  |0   
    Теперь полученное уравнение можно с решить через
дискриминант или теорему Виета. Если бы нам нужно
было бы решить уравнение, в котором степень больше
третьей, то мы искали бы корни до тех пор, пока
не получилось бы уравнение второй степени. 

    Теперь вы готовы.
'''


def stringToList(summ):
    coeff, i, unknown, mistake = [0], 0, '', False
    while summ[0] != '=':  # putting coefficients on the list 
        if "^" in summ:   # find ^ index which will say where the number ends
            b = summ.index('^')
            i = b 
            if not(summ[b + 1].isdigit()):  # user has written not number
                mistake = True
                break

        while summ[i] != '+' and summ[i] != '-' and summ[i] != '=':  # find end of x's end index
            i += 1 
            if i == len(summ) - 1:
                mistake = True
                break

        if coeff == [0] and '^' in summ: # if this is the first cycle add all numbers
                for j in range(int(summ[b + 1]) + 1):
                        coeff.append(0)
                unknown = summ[b - 1]

        if "^" in summ:
            if summ[b + 1: i].isdigit() :
                if summ[0: b - 1] == '' or summ[0: b - 1] == '+':
                    coeff[len(coeff) - int(summ[b + 1: i]) - 1] = 1
                elif summ[0: b - 1] == '-':
                    coeff[len(coeff) - int(summ[b + 1: i]) - 1] = -1
                elif summ[: b - 1].isdigit() or summ[1: b - 1].isdigit():
                    coeff[len(coeff) - int(summ[b + 1: i]) - 1] = int(summ[0: b - 1])
                else:
                    mistake = True
                    break
            else:
                mistake = True
                break 

        elif unknown in summ:
            if summ[0: i - 1] == '' or summ[0:i - 1] == '+':
                coeff[len(coeff) - 2] = 1
            elif summ[0:i - 1] == '-':
                coeff[len(coeff) - 2] = -1
            elif summ[0: i - 1].isdigit() or summ[1: i - 1].isdigit():
                coeff[len(coeff) - 2] = int(summ[0: i - 1])
            else:
                mistake = True
                break

        elif summ[: summ.index('=')].isdigit() or summ[1: summ.index('=')].isdigit():
            coeff[len(coeff) - 1] = int(summ[0: summ.index('=')])  # the last num is left
        else:
            mistake = True
            break
        summ = summ [i:]
        i = 1
        
    return mistake, coeff, unknown


def resutCalc(coeff):
    divs, ko = 0, 1
    coeff_line = 0

    table, korni = [coeff], []  # finding divs of last num and making a table
    last_coeff = abs(table[0][- 1])
    for i in range(1, last_coeff + 1):
        if last_coeff % i == 0:
            table.append([i])
            table.append([-i])


    while (len(table[0]) > 3) and (divs < len(table) - 1):
        while table[divs][ko] != 0 and divs < len(table)-1:
            divs += 1
            for ko in range(1, len(table[0])):
                if ko == 1:
                    table[divs].append(table[coeff_line][1])
                else:
                    table[divs].append(table[divs][0] * table[divs][ko - 1] + table[coeff_line][ko])

        if divs >= len(table) - 1:
            break
        korni.append(table[divs][0])

        for ko in range (1, len(table[0])):
            table[divs - 1][ko] = table[divs][ko]

        table[0] = table[0][:-1]
        table[divs] = table[divs][:1]
        divs -=1
        ko, coeff_line = 1, divs
    
    return table, korni, coeff_line, divs


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