import telebot
import wikipedia
import re

wikipedia.set_lang("ru")

token=''
bot=telebot.TeleBot(token)
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
    bot.send_message(message.chat.id, 'Привет! Меня зовут Юля. Я ищу информацию в Википедии.', reply_markup=keyboard)         
    #bot.send_message(message.chat.id, 'Что вы ищите ?')

@bot.message_handler(commands=['stop'])
def stop_message(message):
	bot.send_message(message.chat.id,'Пока! Возвращайтесь.')

@bot.message_handler(commands=['help'])
def welcome_help(message):
    bot.send_message(message.chat.id, 'Чем я могу Вам помочь?')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id,'Привет! Меня зовут Юля. Я ищу информацию в Википедии.')
        bot.send_message(message.chat.id,' Что Вы ищите ?')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока! Возвращайтесь.')
    elif message.text.lower() == 'спасибо':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Привет', 'Пока')
        bot.send_message(message.chat.id, 'Пожалуйста!', reply_markup=keyboard)
        bot.send_message(message.chat.id, 'Что-то еще?')
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('спасибо')
        titles = ''
        titles = message.text.lower()
        titles_2 = wikipedia.search(titles)
        bot.send_message(message.chat.id, 'Вот что мне удалось найти:')
        #bot.send_message(message.from_user.id, str(titles_2).replace("'", ''))
        bot.send_message(message.chat.id, wikipedia.summary(titles))
        bot.send_message(message.chat.id, 'Чтобы узнать подробнее, нажмите на ссылку ниже')
        bot.send_message(message.chat.id, wikipedia.page(titles).url, reply_markup=keyboard)
        #markup = telebot.types.InlineKeyboardMarkup()
        #markup.add(telebot.types.InlineKeyboardButton(text=str(wikipedia.page(titles).url), url=wikipedia.page(titles).url)) 
        #bot.send_message(message.chat.id, wikipedia.page(titles).url, reply_markup=markup)
        bot.send_message(message.chat.id, 'Если не то что Вы искали попробуйте выбрать из списка ниже:')        
        bot.send_message(message.chat.id, ", ".join(titles_2))
        #markup = telebot.types.InlineKeyboardMarkup()
        #for i in titles_2:
        #    #bot.send_message(message.chat.id, i)
        #    markup.add(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
        #bot.send_message(message.chat.id, 'Выберите из списка, что Вас интересует',reply_markup=markup)
        #bot.send_message(message.chat.id, 'Не понимаю')
        keyboard.row('Привет', 'Пока')
#def handle_text(message):
        #bot.send_message(message.chat.id, getwiki(message.text))

@bot.message_handler(content_types=['photo'])
def text_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Красиво.')

bot.infinity_polling(none_stop=True, interval=0)