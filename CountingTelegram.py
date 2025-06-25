import os
from dotenv import load_dotenv
from pytimeparse import parse
import ptbot


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(bot, chat_id, message_id, total_seconds, secs_left):
    iteration = total_seconds - secs_left
    bar = render_progressbar(total_seconds, iteration)
    text = f"Осталось {secs_left} секунд\n{bar}"
    bot.update_message(chat_id, message_id, text)


def send_time(bot, chat_id):
    bot.send_message(chat_id, "Время вышло!")


def reply(bot, chat_id, text):
    seconds = parse(text)
    if seconds is None or seconds < 0:
        bot.send_message(chat_id, "Не понял время. Пример: 3s, 2m, 1m30s")
        return

    message_id = bot.send_message(chat_id, f"Осталось {seconds} секунд")
    bot.create_countdown(seconds, lambda secs_left: notify_progress(bot, chat_id, message_id, seconds, secs_left))
    bot.create_timer(seconds, lambda: send_time(bot, chat_id))


def main():
    load_dotenv()
    tg_token = os.getenv('TELEGRAM_TOKEN')
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(lambda chat_id, text: reply(bot, chat_id, text))
    bot.run_bot()


if __name__ == '__main__':
    main()