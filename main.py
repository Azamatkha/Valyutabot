import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup,KeyboardButton, ReplyKeyboardMarkup#FOR Creating Button 
import requests
from bs4 import BeautifulSoup#FOR getting data from website "https://nbu.uz"
import re,datetime
#IMPORT Necessary library



tokenapi = 'YOUR TOKEN'
bot = telebot.TeleBot(tokenapi, threaded=False)
user_data = {}

def money():
   url = "https://nbu.uz/uz/exchange-rates/"
   response = requests.get(url)
   if response.status_code == 200:
       soup = BeautifulSoup(response.text, 'html.parser')
       text = soup.get_text()
       pattern = r'(\S+)\s+(\d+\.\d+)'
       matches = re.findall(pattern, text)
       result = []
       for match in matches:
           float_number = match[1]
           result.append(float(float_number))
       result = result[8:][:7]
   return result
#valyuta kurslari ma'lumotlari list ko'rinishida

def date():
    data = str(datetime.datetime.today()).split(' ')
    return data[0]
def mark_up_inline():
    mark_up = InlineKeyboardMarkup()
    mark_up.width = 3
    mark_up.add(InlineKeyboardButton("O'zbekcha🇺🇿", callback_data='uzb'))
    mark_up.add(InlineKeyboardButton("Русский🇷🇺", callback_data='rus'))
    return mark_up

#til uchun inline keyboard

def markup_inline():
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(InlineKeyboardButton("USD🇺🇸➡UZS🇺🇿", callback_data='usduzs'),
               InlineKeyboardButton("UZS🇺🇿➡️USD️🇺🇲", callback_data='uzsusd'))
    markup.add(InlineKeyboardButton("USD🇺🇸➡️RUB🇷🇺", callback_data='usdrub'),
               InlineKeyboardButton("RUB🇷🇺➡USD🇺🇸", callback_data='rubusd'))
    markup.add(InlineKeyboardButton("RUB🇷🇺➡UZS🇺🇿 ", callback_data='rubuzs'),
               InlineKeyboardButton("UZS🇺🇿➡️RUB🇷🇺", callback_data='uzsrub'))
    return markup

#kalkulyator uchun inlinekeyboard
def replymarkup():
    repmu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    repmu.add(KeyboardButton("Xorijiy valyuta kurslari💰"))
    repmu.add(KeyboardButton("Valyuta kalkulyatori🧮"))
    repmu.add(KeyboardButton("Xizmat ko'rsatish🧑🏻‍💻"),KeyboardButton('Bot asoschisi📲'))
    return repmu

#replykeyboard uzbek
def replymarkup2():
    repmu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    repmu.add(KeyboardButton("Курсы обмена валют💰"))
    repmu.add(KeyboardButton("Валютный калькулятор🧮"))
    repmu.add(KeyboardButton("Услуга🧑🏻‍💻"), KeyboardButton('Основатель бота📲'))
    return repmu

#replykeyboard rus

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, f"Tilni tanlang\nВыберите язык\n", reply_markup=mark_up_inline())
    # bot.reply_to(message,f"""Salom {message.from_user.first_name}, botimizga xush kelibsiz,\nBu bot sizga chet el valyutalarini o'zbek so'miga \nnisbatini bilib olishingizga yordam beradi.""",reply_markup=markup_inline()

@bot.callback_query_handler(func=lambda call: call.data.startswith('uzb') or call.data.startswith('rus'))
def calllback_query(call):
    if call.data.startswith('uzb'):
        bot.answer_callback_query(call.id, "O'zbek tili🇺🇿 tanlandi")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"Assalomu alaykum, foydalanuvchi.\nXush kelibsiz.", reply_markup=replymarkup())
    elif call.data.startswith('ru'):
        bot.answer_callback_query(call.id, "Выбран русский язык🇷🇺")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"Приветствую, пользователь.\nДобро пожаловать.", reply_markup=replymarkup2())
#
@bot.message_handler(func=lambda message: message.text == "Xorijiy valyuta kurslari💰")
def press_rep(message):
    usd = f"1 USD🇺🇸 AQSH dollari - {int(money()[0])} so'm"
    rub = f"1 RUB🇷🇺 Rassiya rubli - {int(money()[2])} so'm"
    eur = f"1 EUR🇪🇺 Yevro - {int(money()[1])} so'm"
    gbp = f"1 GBP🇬🇧 Britaniya funt sterlingi - {int(money()[3])} so'm"
    chf = f"1 CHF🇨🇭 Shvetsariya franki - {int(money()[4])} so'm"
    jpy = f"1 JPY🇯🇵 Yaponiya iyenasi - {int(money()[5])} so'm"
    kzt = f"1 KZT🇰🇿 Qozog‘iston tengesi - {int(money()[6])} so'm"
    bot.send_message(message.chat.id,f"Bugungi valyuta kurslari💰\t{date()}:\n{usd}\n{rub}\n{eur}\n{gbp}\n{chf}\n{jpy}\n{kzt}")

@bot.message_handler(func=lambda message: message.text == "Xizmat ko'rsatish🧑🏻‍💻" )
def services(message):
    bot.send_message(message.chat.id,"Reklama xizmati📩<a href='https://web.telegram.org/k/#@axeabytead_bot'>@axeabytead_bot</a>",parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == "Услуга🧑🏻‍💻" )#or message.text == "Xizmat ko'rsatish🧑🏻‍💻"
def service(message):
    bot.send_message(message.chat.id,"Рекламный сервис📩<a href='https://web.telegram.org/k/#@axeabytead_bot'>@axeabytead_bot</a>",parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == 'Bot asoschisi📲' or message.text == 'Основатель бота📲' )
def creator(message):
    bot.send_message(message.chat.id,"<a href='https://t.me/the_azamatkh'>Creator🧑🏻‍💻</a>",parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == "Курсы обмена валют💰")
def press_rep(message):
    bot.send_message(message.chat.id,requests.get("https://nbu.uz/uz/exchange-rates/").status_code)
    usd = f"1 USD🇺🇸 доллар США - {int(money()[0])} сумов"
    rub = f"1 RUB🇷🇺 Русский рубль - {int(money()[2])} сумов"
    eur = f"1 EUR🇪🇺 Евро - {int(money()[1])} сумов"
    gbp = f"1 GBP🇬🇧 Британский фунт стерлингов - {int(money()[3])} сумов"
    chf = f"1 CHF🇨🇭 Швейцарский франк - {int(money()[4])} сумов"
    jpy = f"1 JPY🇯🇵 Японская иена - {int(money()[5])} сумов"
    kzt = f"1 KZT🇰🇿 Казахский тенге - {int(money()[6])} сумов"
    bot.send_message(message.chat.id,f"Сегодняшние курсы обмена💰\t{date()}:\n{usd}\n{rub}\n{eur}\n{gbp}\n{chf}\n{jpy}\n{kzt}")

@bot.message_handler(func=lambda message: message.text == "Valyuta kalkulyatori🧮")
def calculateuz(message):
    bot.send_message(message.chat.id,"Tanlang:",reply_markup=markup_inline())

@bot.message_handler(func=lambda message: message.text == "Валютный калькулятор🧮")
def calculateuz(message):
    bot.send_message(message.chat.id,"Выбирать:",reply_markup=markup_inline())


@bot.callback_query_handler(func=lambda call: call.data.startswith('usd') or call.data.startswith('uzs') or call.data.startswith('rub'))
def handle_conversion_option(call):
    user_id = call.from_user.id
    user_data[user_id] = {'option': call.data, 'number': None}
    bot.answer_callback_query(call.id, f"{call.data.upper()}✅")
    bot.send_message(call.message.chat.id, "Valyuta miqdorini kiriting:\nВведите сумму в валюте:")

@bot.message_handler(func=lambda message: True)
def handle_number(message):
    user_id = message.from_user.id
    # bot.send_message(message.chat.id,user_id)
    if user_id in user_data:
        try:
            number = int(message.text)
            option = user_data[user_id]['option']
            del user_data[user_id]  # Remove user data to reset the state
            if option == 'usduzs':
                result = number * float(money()[0])
                bot.send_message(message.chat.id, f"{number}$ = {result:.2f}so'm")
            elif option == 'uzsusd':
                result = number / float(money()[0])
                bot.send_message(message.chat.id, f"{number}so'm = {result:.2f}$")
            elif option == 'rubuzs':
                result = number * float(money()[2])
                bot.send_message(message.chat.id, f"{number}₽ = {result:.2f}so'm")
            elif option == 'uzsrub':
                result = number / float(money()[2])
                bot.send_message(message.chat.id, f"{number}so'm = {result:.2f}₽")
            elif option == 'usdrub':
                result = number * float(money()[0]/money()[2])
                bot.send_message(message.chat.id, f"{number}$ = {result:.2f}₽")
            elif option == 'rubusd':
                result = number / float(money()[0]/money()[2])
                bot.send_message(message.chat.id, f"{number}₽ = {result:.2f}$")
            else:
                bot.send_message(message.chat.id, "Noto'g'ri variant. Iltimos, qayta urinib ko'ring.\nНеверный вариант. Пожалуйста, попробуйте еще раз")
        except ValueError:
            bot.send_message(message.chat.id, ".Yaroqsiz kiritish. Yaroqli raqam kiriting.\nНеверный Ввод. Пожалуйста, введите корректное число.")
    else:
        bot.send_message(message.chat.id, "Iltimos, avval konvertatsiya variantini tanlang.\nСначала выберите вариант преобразования.")

# bot.remove_webhook()
bot.polling()
