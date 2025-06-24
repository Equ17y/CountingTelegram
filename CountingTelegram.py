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


def make_reply(bot):
    def reply(chat_id, text):
        seconds = parse(text)
        if seconds is None or seconds < 0:
            bot.send_message(chat_id, "Не понял время. Пример: 3s, 2m, 1m30s")
            return

        message_id = bot.send_message(chat_id, f"Осталось {seconds} секунд")


        def notify_progress(secs_left):
            elapsed = seconds - secs_left
            bar = render_progressbar(seconds, elapsed)
            text = f"Осталось {secs_left} секунд\n{bar}"
            bot.update_message(chat_id, message_id, text)


        def send_time():
            bot.send_message(chat_id, "Время вышло!")

        bot.create_countdown(seconds, notify_progress)
        bot.create_timer(seconds, send_time)

    return reply


def main():
    load_dotenv()
    tg_token = os.getenv('TELEGRAM_TOKEN')
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(make_reply(bot))
    bot.run_bot()


if __name__ == '__main__':
    main()