import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])  # Обработчик команды /start
def send_welcome(message):
    text = (
        "Добро пожаловать! Это бот для конвертации валют.\n"
        "Напишите через пробел:\n"
        "<имя валюты> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n"
        "Например: USD EUR 100\n"
        "Для просмотра доступных валют введите /values"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])  # Обработчик команды /values
def values(message):
    text = "Доступные валюты: Евро (EUR), Доллар США (USD), Российский рубль (RUB)"
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])  # Обработка запроса на конвертацию валют
def convert(message):
    try:
        user_input_values = message.text.split(' ')  # Разбиваем сообщение пользователя на три части
        if len(user_input_values) != 3:
            raise APIException("Пожалуйста, используйте формат: <валюта1> <валюта2> <количество> через пробел.")

        base, quote, amount = user_input_values
        total = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать запрос.\n{e}")
    else:
        text = f"Цена {amount} {base.upper()} в {quote.upper()} — {total}"
        bot.reply_to(message, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
