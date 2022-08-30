from email import message
from debugpy import connect
import telebot
from telebot import types
import sqlite3


level = 0
level5w = 0

bot = telebot.TeleBot(
    "5434878518:AAEbcqZpqITA_89lMNzuD16KWs9XdzNWRfs", parse_mode=None)

commands = {
    "start": "Привет, хочешь начать изучение грузинского алфавита? "
    "напиши Да/нет:",
    "start2": "Привет, ты уже у нас был, начнем с твоего прошлого уровня? "
    "напиши Да/нет:",
    "help": "To start learning you should "
    "add words to your dictionary by typing /addwords.\n"}

levels = [
    {"send": "Вот тебе новая буква 'ი', на русском звучит как 'и' ", "expected_answer": "ი"},
    {"send": "Вот тебе новая буква 'ა', на русском звучит как 'а' ", "expected_answer": "ა"},
    {"send": "Вот тебе новая буква 'თ', на русском звучит как 'т'  ", "expected_answer": "თ"},
    {"send": "Вот тебе новая буква 'ს', на русском звучит как 'c'  ", "expected_answer": "ს"},
    {"send": "Вот тебе новая буква 'ხ', на русском звучит как 'х'  ", "expected_answer": "ხ"}
]

levels_library_letters = [
    {"level": "1 уровень", "letters": {"и": 'ი'}  },
    {"level": "2 уровень", "letters": {"а":	'ა'}  },
    {"level": "3 уровень", "letters": {"т": 'თ'}  },
    {"level": "4 уровень", "letters": {"с": 'ს'}  },
    {"level": "5 уровень", "letters": {"х": 'ხ'}  },
    {"level": "6 уровень", "letters": {"х": 'ხ'}  }
]

levels_words = [
    {"send": "На грузинском 'фиалка' это 'ია' и звучит как 'иа' ", "expected_answer": "ია"},
    {"send": "На грузинском 'палец' это 'თითი' и звучит как 'тити' ", "expected_answer": "თითი"},
    {"send": "На грузинском 'часы' это 'საათი' и звучит как 'са-а-ти' ", "expected_answer": "საათი"},
    {"send": "На грузинском 'коза' это 'თხა' и звучит как 'ткха' ", "expected_answer": "თხა"},
    {"send": "На грузинском 'глина' это 'თიხა' и звучит как 'ти-кха' ", "expected_answer": "თიხა"}
]


levels_library_words_to_check = [
    {"level": "1 уровень", "word": {"фиалка": 'ია'}  },
    {"level": "2 уровень", "word": {"":	'ა'}  },
    {"level": "3 уровень", "word": {"": 'თ'}  },
    {"level": "4 уровень", "word": {"": 'ს'}  }
]




# Keyboards

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
itembtna = types.KeyboardButton('ი')
itembtnv = types.KeyboardButton('ა')
itembtnc = types.KeyboardButton('თ')
itembtnd = types.KeyboardButton('ს')
itembtne = types.KeyboardButton('ხ')
markup.row(itembtna, itembtnv)
markup.row(itembtnc, itembtnd, itembtne)


# markup_next = types.ReplyKeyboardMarkup(one_time_keyboard=True)
# itembtnazad = types.KeyboardButton('Напомни попозже')
# itembtnvpered = types.KeyboardButton('да')
# markup_next.row(itembtnazad, itembtnvpered)


markup_privet = telebot.types.InlineKeyboardMarkup(row_width=2)
markup_privet.add(telebot.types.InlineKeyboardButton(text='Давай попозже',callback_data='нет'))
markup_privet.add(telebot.types.InlineKeyboardButton(text='Да, начинаем!😎',callback_data='да'))


markup_next_bukva = telebot.types.InlineKeyboardMarkup(row_width=2)
markup_next_bukva.add(telebot.types.InlineKeyboardButton(text='Давай попозже',callback_data='нет'))
markup_next_bukva.add(telebot.types.InlineKeyboardButton(text='Да, идем дальше!👉',callback_data='да кидай буквы'))

markup_next_text = telebot.types.InlineKeyboardMarkup(row_width=2)
markup_next_text.add(telebot.types.InlineKeyboardButton(text='Давай попозже',callback_data='нет'))
markup_next_text.add(telebot.types.InlineKeyboardButton(text='Да, идем дальше!👉',callback_data='да кидай текст'))

markup_next_proverka = telebot.types.InlineKeyboardMarkup(row_width=2)
markup_next_proverka.add(telebot.types.InlineKeyboardButton(text='Давай попозже',callback_data='нет'))
markup_next_proverka.add(telebot.types.InlineKeyboardButton(text='Да, идем дальше!👉',callback_data='да кидай проверку'))

markup_next_words5bukv = telebot.types.InlineKeyboardMarkup(row_width=2)
markup_next_words5bukv.add(telebot.types.InlineKeyboardButton(text='Давай попозже',callback_data='нет'))
markup_next_words5bukv.add(telebot.types.InlineKeyboardButton(text='Да, учим слова!👉',callback_data='да кидай слова из 5 букв'))


#Database


# @bot.message_handler(commands=['start'])
# def welcome(message):
#     mesg = bot.send_message(message.chat.id, commands["start"])
#     bot.register_next_step_handler(mesg, receive_da_start)

@bot.message_handler(commands=['start'])
def welcome(message):
    global level

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users_id_lvl(
        id INTEGER, level INTEGER, level2 INTEGER
        )""")

    connect.commit()

    id_to_check = message.chat.id
    cursor.execute(f"SELECT id FROM users_id_lvl WHERE id = {id_to_check}")
    data = cursor.fetchone()
    if data is None:
        user_id = message.chat.id
        level = 0
        cursor.execute("INSERT INTO users_id_lvl (id,level) VALUES(?,?);",(user_id,level))
        connect.commit()
        
        # mesg = bot.send_message(message.chat.id, commands["start"])
        bot.send_message(message.chat.id, "Готов приступить?👋", reply_markup=markup_privet)
        # bot.register_next_step_handler(mesg, receive_da_start)

    else:
        id = message.chat.id
        cursor.execute("SELECT * FROM users_id_lvl WHERE id=?", (id,))
        user_data = cursor.fetchone()
        level = user_data[1]
        print(level)
        
        mesg = bot.send_message(message.chat.id, commands["start2"], reply_markup=markup_next_bukva)
        bot.register_next_step_handler(mesg, callback2)


@bot.message_handler(commands=['delete'])
def delete(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    id_to_delete = message.chat.id
    cursor.execute(f"DELETE FROM users_id_lvl WHERE id = {id_to_delete}")
    connect.commit()
    bot.send_message(message.chat.id, "Ты удален из базы")


# def receive_da_start(message):
#     print('receivedastra')
#     if message.text == "да":
#         mesg = bot.send_message(message.chat.id, "Олично, буду присылать тебе грузинские буквы, тексты, и слова, запоминай!, Пиши 'да' если идем дальше")
#         bot.send_message(message.chat.id, "Идём дальше?", reply_markup=markup)
#         bot.register_next_step_handler(mesg, send_task)

@bot.callback_query_handler(func=lambda call: call.data == "да")
def callback(call):
    if call.message:
        if call.data == 'да':
            print('callaback')
            mesg = bot.send_message(call.message.chat.id,'Олично, буду присылать тебе грузинские буквы, тексты, и слова, запоминай!')
            # bot.register_next_step_handler(mesg, send_task)
            bot.send_message(call.message.chat.id,'Если видишь клавиатуру и готов идти дальше, жми "Идём дальше"',reply_markup=markup_next_bukva)

            

# @bot.callback_query_handler(func=lambda call: call.data == "нет")
# def callback(call):
#     if call.message:
#         if call.data == 'нет':
#             print('callaback2')
#             mesg = bot.send_message(call.message.chat.id,'Отлчино лови буквы')
#             bot.register_next_step_handler(mesg, send_task)
#             bot.send_message(call.message.chat.id,'вот клавиатура',reply_markup=markup_next2)            
        

@bot.callback_query_handler(func=lambda call: call.data == "да кидай буквы")
def callback2(call):
    if call.message:
        if call.data == 'да кидай буквы':
            sms = levels[level]["send"]
            msg = bot.send_message(call.message.chat.id, sms)
            bot.send_message(call.message.chat.id,"Жми дальше, чтобы получить текст с этой буквой",reply_markup=markup_next_text)
            bot.register_next_step_handler(msg, send_task2)
            

@bot.callback_query_handler(func=lambda call: call.data == "да кидай текст")
def send_task2(call):
    if call.message:
        if call.data == 'да кидай текст':
            text = "привет как дела что делаешь сучка"
            text = text.split()
            sms = None

            for i in range(len(text)):
                for rus_letter in levels_library_letters[level]["letters"]:
                    geo_letter = levels_library_letters[level]["letters"][rus_letter]
                    text[i] = text[i].replace(rus_letter,geo_letter)
            sms = " ".join(text)

            msg = bot.send_message(call.message.chat.id,sms)
            bot.send_message(call.message.chat.id,"Жми дальше, если готов получить небольшую проверку",reply_markup=markup_next_proverka)
            bot.register_next_step_handler(msg,proverka2)


@bot.callback_query_handler(func=lambda call: call.data == "да кидай проверку")
def proverka2(call):
    global level
    if call.message:
        if call.data == 'да кидай проверку':
            for letter in levels_library_letters[level]["letters"]:
                message_s_bukva = f"Какой грузинской букве соответсвует, русская {letter}"
                msg = bot.send_message(call.message.chat.id, message_s_bukva)
                bot.register_next_step_handler(msg, check_otvet2)
                bot.send_message(call.message.chat.id, "Нажми", reply_markup=markup)




# def send_task2(message):
#     if message.text == "да":

#         text = "привет как дела что делаешь сучка"
#         text = text.split()
#         sms = None

#         for i in range(len(text)):
#             for rus_letter in levels_library_letters[level]["letters"]:
#                 geo_letter = levels_library_letters[level]["letters"][rus_letter]
#                 text[i] = text[i].replace(rus_letter,geo_letter)
#         sms = " ".join(text)

#         msg = bot.send_message(message.chat.id,sms)
#         bot.send_message(message.chat.id,"Пиши да если идем дальше")
#         bot.register_next_step_handler(msg,proverka2)

#     else:
#         bot.send_message(message.chat.id, "Davai eshe okey")
#         send_task(message)





# def send_task(message):
#             print('send_task') 
#             sms = levels[level]["send"]
#             msg = bot.send_message(message.chat.id, sms)
#             bot.send_message(message.chat.id,"Пиши да, чтобы получить текст с этой буквой")
#             bot.register_next_step_handler(msg, send_task2)



#проверка с русского на грузинский - 2 функции

# def proverka2(message):
#     global level

#     for letter in levels_library_letters[level]["letters"]:
#         message_s_bukva = f"Какой грузинской букве соответсвует, русская {letter}"
#         msg = bot.send_message(message.chat.id, message_s_bukva)
#         bot.register_next_step_handler(msg, check_otvet2)
#         bot.send_message(message.chat.id, "Нажми", reply_markup=markup)
        
def check_otvet2(message):
    global level
    if message.text == levels[level]["expected_answer"]:
        level = level + 1
        # level2 = ("level",)
        level2 = str(level)
        user_id = message.chat.id
         # Send to database сurrent level
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()

        # cursor.execute("INSERT INTO users_id_lvl (level2) VALUES(?);",(level2))
        cursor.execute("UPDATE users_id_lvl SET level=? WHERE id=?",(level2, user_id))
        
        connect.commit()

        if level < 5:
            bot.send_message(message.chat.id, "Верно, молодец!",reply_markup=markup_next_bukva)
        if level == 5:
            msg = bot.send_message(message.chat.id, "Верно, молодец! Ты уже выучил 5 букв, давай выучим несколько слов",reply_markup=markup_next_words5bukv)
        

    else:
        msg = bot.send_message(message.chat.id, "Вот и нет, давай еще раз",reply_markup=markup)
        bot.register_next_step_handler(msg, check_otvet2)      


@bot.callback_query_handler(func=lambda call: call.data == "да кидай слова из 5 букв")
def words5bukv(call):
    global level5w
    if call.message:
        if call.data == 'да кидай слова из 5 букв':
            if level5w < 5:
                sms = levels_words[level5w]["send"]
                msg = bot.send_message(call.message.chat.id, sms)
                level5w = level5w + 1
                bot.send_message(call.message.chat.id,"Жми дальше, учим слова на грузинском",reply_markup=markup_next_words5bukv)
                bot.register_next_step_handler(msg, send_task2)
            else:
                bot.send_message(call.message.chat.id,"Отлично ты выучил часть новых слов, давай проверим их",reply_markup=markup_next_words5bukv)




#проверка с грузинского на русский - 2 функции 

# def proverka(message):
#     global level

#     for letter in levels_library_letters[level]["letters"]:
#         geor_letter = levels_library_letters[level]["letters"][letter]

#         message_s_bukva = f"Какой русской букве соответсвует, грузинская {geor_letter}"
#         msg = bot.send_message(message.chat.id, message_s_bukva)
#         bot.register_next_step_handler(msg, check_otvet)
        

# def check_otvet(message):
#     global level
#     if message.text == levels[level]["expected_answer"]:
#         level = level + 1
#         bot.send_message(message.chat.id, "Верно, молодец!")
#         send_task(message)
        

#     else:
#         msg = bot.send_message(message.chat.id, "Davai eshe")
#         bot.register_next_step_handler(msg, check_otvet)

# def receive_answer(message):
#     global level
#     if message.text == levels[level]["expected_answer"]:
#         send_task(message)
#         level = level + 1 
#     else:
#         msg = bot.send_message(message.chat.id, "Davai eshe")
#         bot.register_next_step_handler(msg, receive_answer)


# def answer_check_letter (message):
#     global level
#     if message.text == levels[level]["expected_answer"]:
#         level = level + 1
#         answer_check_letter(message)
#     else:
#         msg = bot.send_message(message.chat.id, "Davai eshe")
#         bot.register_next_step_handler(msg, answer_check_letter)




bot.infinity_polling()