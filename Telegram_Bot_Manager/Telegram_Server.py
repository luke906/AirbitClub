import telegram

if __name__ == "__main__":

    bot = telegram.Bot(token='538038697:AAHELqBNpIBU7RYQRCsC1JRonblnrN0vfLs')

    updates = bot.get_updates()
    for u in updates:
        print(u.message)
