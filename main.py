import json
import os
from datetime import date, datetime
from random import choice, seed

import telebot

seed(datetime.now().timestamp())

TOKEN = os.environ['TgBot23_48_TOKEN']
CHANNEL_ID = int(os.environ['TgBot23_48_CHANNEL_ID'])


def load_config() -> dict:
    raw = os.environ.get('TgBot23_48_CONFIG')
    if raw:
        return json.loads(raw)
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), encoding='utf-8') as f:
        return json.load(f)


def plural_days(n: int) -> str:
    days = ['день', 'дня', 'дней']
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2
    return f'{n} {days[p]}'


def choice_message(section: dict) -> str:
    return f"{choice(section['actions'])}{choice(section['additions'])}"


def calculate_days_count(since: date) -> int:
    now = datetime.now().date()
    return (now - since).days


def generate_message(section: dict) -> str:
    since = date.fromisoformat(section['since'])
    days_count = calculate_days_count(since)
    if section.get('countdown'):
        days_count = -days_count
    return f'{choice_message(section)} {plural_days(days_count)}'


def main() -> str:
    config = load_config()
    lines = [generate_message(section) for section in config['sections']]
    msg = '\n'.join(lines)
    print(msg)
    return msg


def cronjob() -> None:
    bot = telebot.TeleBot(TOKEN)
    msg = main()
    bot.send_message(CHANNEL_ID, msg, parse_mode='Markdown')


if __name__ == '__main__':
    cronjob()
