import requests
from requests.auth import HTTPBasicAuth
import json
from config import XE_USERNAME, XE_PASSWORD


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        base = base.upper()
        quote = quote.upper()

        if base == quote:
            raise APIException("Нельзя конвертировать одну и ту же валюту.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество: {amount}")

        url = 'https://xecdapi.xe.com/v1/convert_from'  # XE.com API
        params = {
            'from': base,
            'to': quote,
            'amount': amount
        }

        try:
            response = requests.get(url, auth=HTTPBasicAuth(XE_USERNAME, XE_PASSWORD), params=params)

            if response.status_code != 200:  # проверяем если запрос был успешным
                raise APIException(f"Ошибка при запросе API: {response.status_code}")

            data = response.json()  # Парсим ответ

            if "error" in data:
                raise APIException(data["error"])

            total = data['to'][0]['mid']  # По документации XE.com mid это нужное нам значение
            return total
    # К сожалению Free Trial подразумевает Mock rates то есть шуточные значения, то есть всегда 12345 в разных видах :(
    # Но если оплатить платную подписку ценой всего-то в 800$ в год, то бот начнет выдавать реальные курсы валют :)
        except requests.RequestException as e:
            raise APIException(f"Ошибка запроса: {e}")
        except json.JSONDecodeError:
            raise APIException("Не удалось обработать ответ от API.")
