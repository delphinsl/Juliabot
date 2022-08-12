import os
import telebot
import wikipedia
import random
import re
from datetime import date
import requests
import urllib.request
#import locale
import phonenumbers
#from phonenumbers import geocoder
#from phonenumbers import timezone
#from phonenumbers import carrier

"""
#для распознавания речи
#import requests
import speech_recognition as sr
import subprocess
import datetime
import ffmpeg
import soundfile as sf
"""

wikipedia.set_lang("ru")
#locale.setlocale(category=locale.LC_ALL, 'ru_RU.UTF-8')
#local = locale.getlocale()
#token='5440755797:AAFrtl3HrvgNy-apBgltxngfMkF-ZX9y88g'
#bot=telebot.TeleBot(token)
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

#bot.remove_webhook()
#bot.set_webhook("YOUR_URL")
#bot.remove_webhook()
#bot.set_webhook("https://d5d0gd6j7e56ndj8nc18.apigw.yandexcloud.net")

months = {
    'January' : 'января',
    'February' : 'февраля',
    'March' : 'марта',
    'April' : 'апреля',
    'May' : 'мая',
    'June' : 'июня',
    'July' : 'июля',
    'August' : 'августа',
    'September' : 'сентября',
    'October' : 'октября',
    'November' : 'ноября',
    'December' : 'декабря'
    }
"""
# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'
"""
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Привет', 'Пока')
    #bot.send_message(message.chat.id, 'Привет! Меня зовут Юля. Я ищу информацию в Википедии.', reply_markup=keyboard)         
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}! Меня зовут Юля. Я ищу информацию в Википедии.', reply_markup=keyboard)
    buttons = [
        telebot.types.InlineKeyboardButton(text = 'Русский язык', callback_data = 1),
        telebot.types.InlineKeyboardButton(text = 'Английский язык', callback_data = 2)
        ]
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(*buttons)
    bot.send_message(message.chat.id, text = 'Выберите язык для поиска', reply_markup=markup)


@bot.message_handler(commands=['stop'])
def stop_message(message):
	bot.send_message(message.chat.id,'Пока! Возвращайтесь.')

@bot.message_handler(commands=['help'])
def welcome_help(message):
    bot.send_message(message.chat.id, 'Я знаю какой сегодня день и могу найти какой праздник в этот день. Чем я могу Вам помочь?')

@bot.message_handler(commands=['ru'])
def welcome_help(message):
    wikipedia.set_lang("ru")
    bot.send_message(message.chat.id, 'Установлен русский язык')

@bot.message_handler(commands=['en'])
def welcome_help(message):
    wikipedia.set_lang("en")
    bot.send_message(message.chat.id, 'Установлен английский язык')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() in ['привет','здравствуйте', 'добрый день', 'hello', 'hi', 'здорово', 'салют']:
        list_hi = ['Привет', 'Здравствуйте']
        #bot.send_message(message.chat.id, random.choice(list_hi)+' Меня зовут Юля. Я ищу информацию в Википедии.')
        bot.send_message(message.chat.id, random.choice(list_hi)+' '+ message.from_user.first_name +'! Меня зовут Юля. Я ищу информацию в Википедии.')
        bot.send_message(message.chat.id,' Что Вы ищите ?')
    elif message.text.lower() in ['пока','до свидания', 'до встречи','счастливо','прощай','пока пока']:
        list_bye = ['Пока! Возвращайтесь.', 'До свидания!', 'До скорой встречи!']
        bot.send_message(message.chat.id, random.choice(list_bye))
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Поддержать проект', url='https://netmonet.ru/s/user4150'))        
        bot.send_message(message.chat.id, 'Спасибо, что воспользовались ботом!', reply_markup=markup)
    elif message.text.lower() == 'спасибо':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Привет', 'Пока')
        bot.send_message(message.chat.id, 'Пожалуйста!', reply_markup=keyboard)
        bot.send_message(message.chat.id, 'Что-то еще?')
    elif message.text.lower() in ['кто твой создатель', 'кто тебя сделал', 'кто разработчик', 'кто тебя создал']:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Привет', 'Пока')
        bot.send_contact(message.chat.id, '+79160962320','Виталий')
    elif message.text.lower() in ['какой сегодня день', 'какой день сегодня', 'какой сегодня праздник', 'какой праздник сегодня', 'какой сегодня день?', 'какой день сегодня?', 'какой сегодня праздник?', 'какой праздник сегодня?']:
        day = message.text
        current_date = date.today()      
        current_date_today = current_date.strftime('%d %B %Y').split(' ')
        month = months[current_date_today[1]]
        current_date_today = f'{current_date_today[0]} {month} {current_date_today[2]}'
        if message.text.lower() in ['какой сегодня день', 'какой день сегодня', 'какой сегодня день?', 'какой день сегодня?']:
            bot.send_message(message.chat.id, f'Сегодня {current_date_today}')
        elif message.text.lower() in ['какой сегодня праздник', 'какой праздник сегодня', 'какой сегодня праздник?', 'какой праздник сегодня?']:
            try:
                current_date = current_date.strftime(f'%d {month}')
                holiday = 'праздник ' + current_date                
                bot.send_message(message.chat.id, wikipedia.summary(holiday))
            except Exception as e:
                bot.send_message(message.chat.id, f'В энциклопедии нет информации об этом {holiday}')
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('спасибо')
        titles = ''
        titles = message.text.lower()
        titles_2 = wikipedia.search(titles)
        try:
            #bot.send_message(message.chat.id, 'Вот что мне удалось найти:')
            #bot.send_message(message.from_user.id, str(titles_2).replace("'", ''))
            bot.send_message(message.chat.id, 'Вот что мне удалось найти:\n\n' + wikipedia.summary(titles))
            bot.send_message(message.chat.id, 'Чтобы узнать подробнее, нажмите на ссылку ниже')
            bot.send_message(message.chat.id, urllib.parse.unquote(wikipedia.page(titles).url), reply_markup=keyboard)
            #bot.send_message(message.chat.id, wikipedia.page(titles).url, reply_markup=keyboard)
            #markup = telebot.types.InlineKeyboardMarkup()
            #markup.add(telebot.types.InlineKeyboardButton(text=str(wikipedia.page(titles).url), url=wikipedia.page(titles).url)) 
            #bot.send_message(message.chat.id, wikipedia.page(titles).url, reply_markup=markup)
            bot.send_message(message.chat.id, 'Если не то, что Вы искали, попробуйте выбрать из списка ниже:')
            bot.send_message(message.chat.id, ", ".join(titles_2))
        except Exception as e:
            bot.send_message(message.chat.id, 'В энциклопедии нет информации об этом')
            #markup = telebot.types.InlineKeyboardMarkup()
            #for i in titles_2:
            #    #bot.send_message(message.chat.id, i)
            #    markup.add(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
            #bot.send_message(message.chat.id, 'Выберите из списка, что Вас интересует',reply_markup=markup)
            #bot.send_message(message.chat.id, 'Не понимаю')
        keyboard.row('Привет', 'Пока')
#def handle_text(message):
        #bot.send_message(message.chat.id, getwiki(message.text))

#функция ответа на фото
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    bot.send_message(message.chat.id, 'Красиво.')

#функция ответа на стикер
@bot.message_handler(content_types=['sticker'])
def sticker_handler(message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)

#функция ответа на локацию
@bot.message_handler(content_types=['location'])
def loc_handler(message):
    bot.send_message(message.chat.id, 'Вы здесь, а я повсюду')

#функция ответа на контакт
@bot.message_handler(content_types=['Contact'])
def cont_handler(message):
    number_phone = message.contact.phone_number
    if not number_phone.startswith('+'):
        number_phone = (number_phone).replace('8', '+7', 1)
    number_phone = phonenumbers.parse(number_phone, 'ru')
    country = phonenumbers.geocoder.description_for_number(number_phone, 'ru')
    provider = phonenumbers.carrier.name_for_number(number_phone, 'ru')    
    try:
        if country =='' and provider !='':
            bot.send_message(message.chat.id, f'Оператор: {provider}')
        elif country !='' and provider =='':
            bot.send_message(message.chat.id, f'Регион: {country}')
        elif country !='' and provider !='':
            bot.send_message(message.chat.id, f'Регион: {country}, оператор: {provider}')
        else:
            bot.send_message(message.chat.id, f'Неизвестный формат номера {number_phone}') 
    except Exception as e:
        bot.send_message(message.chat.id, f'Что-то пошло не так')

#функция ответа на другие типы документов
@bot.message_handler(content_types=['audio', 'voice', 'video', 'document'])
def any_handler(message):
    bot.send_message(message.chat.id, 'Я не знаю, что с этим делать. Что Вы ищите?')

#функция выбора языка для поиска в википедии
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == '1':
        wikipedia.set_lang("ru")
        bot.send_message(call.message.chat.id, 'Установлен русский язык')
    elif call.data == '2':
        wikipedia.set_lang("en")
        bot.send_message(call.message.chat.id, 'Установлен английский язык')
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, 'Что вы ищите ?')

"""
###
def audio_to_text(dest_name: str):
# Функция для перевода аудио, в формате ".wav" в текст
    r = sr.Recognizer() # такое вообще надо комментить?
    # тут мы читаем наш .wav файл
    message = sr.AudioFile(dest_name)
    with message as source:
        audio = r.record(source)
    result = r.recognize_google(audio, language="ru_RU") # используя возможности библиотеки распознаем текст, так же тут можно изменять язык распознавания
    return result


#функция распознавания речи
@bot.message_handler(content_types=['voice'])
def get_audio_messages(message):
# Основная функция, принимает голосовуху от пользователя
    try:
        print("Started recognition...")
        # Ниже пытаемся вычленить имя файла, да и вообще берем данные с мессаги
        file_info = bot.get_file(message.voice.file_id)
        #path = file_info.file_path # Вот тут-то и полный путь до файла (например: voice/file_2.oga)
        path = os.path.splitext(file_info.file_path)[0]
        print(path)
        fname = os.path.basename(path) # Преобразуем путь в имя файла (например: file_2.oga)
        doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path)) # Получаем и сохраняем присланную голосвуху (Ага, админ может в любой момент отключить удаление айдио файлов и слушать все, что ты там говоришь. А представь, что такую бяку подселят в огромный чат и она будет просто логировать все сообщения [анонимность в телеграмме, ахахаха])
        with open(fname+'.oga', 'wb') as f:
            f.write(doc.content) # вот именно тут и сохраняется сама аудио-мессага
        process = subprocess.run(['ffmpeg', '-i', fname+'.oga', fname+'.wav'])# здесь используется страшное ПО ffmpeg, для конвертации .oga в .wav
        result = audio_to_text(fname+'.wav') # Вызов функции для перевода аудио в текст
        bot.send_message(message.from_user.id, format(result)) # Отправляем пользователю, приславшему файл, его текст
    except sr.UnknownValueError as e:
        # Ошибка возникает, если сообщение не удалось разобрать. В таком случае отсылается ответ пользователю и заносим запись в лог ошибок
        bot.send_message(message.from_user.id,  "Прошу прощения, но я не разобрал сообщение, или оно поустое...")
        #with open(logfile, 'a', encoding='utf-8') as f:
        #    f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) +':'+ str(message.from_user.language_code) + ':Message is empty.\n')
    except Exception as e:
        # В случае возникновения любой другой ошибки, отправляется соответствующее сообщение пользователю и заносится запись в лог ошибок
        bot.send_message(message.from_user.id,  "Что-то пошло через жопу, но наши смелые инженеры уже трудятся над решением... \nДа ладно, никто эту ошибку исправлять не будет, она просто потеряется в логах.")
        #with open(logfile, 'a', encoding='utf-8') as f:
        #    f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) +':'+ str(message.from_user.language_code) +':' + str(e) + '\n')
    finally:
        # В любом случае удаляем временные файлы с аудио сообщением
        os.remove(fname+'.wav')
        os.remove(fname+'.oga')
###
"""

# ---------------- local testing ----------------
if __name__ == '__main__':
    bot.infinity_polling(one_stop=True, interval=0)

#bot.infinity_polling(none_stop=True, interval=0)
