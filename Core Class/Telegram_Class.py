
import telegram # https://pypi.python.org/pypi/python-telegram-bot#installing

class Telegram_Manager:

    def __init__(self, user_id):
        #self.bot = telegram.Bot(token='453642591:AAFwBdO7CaZ4XpfYi1ud3b6nURjYisHgs-s')
        self.bot = telegram.Bot(token='538038697:AAHELqBNpIBU7RYQRCsC1JRonblnrN0vfLs')

        #self.updates = self.bot.getUpdates()  # 업데이트 내역을 받아옵니다.
        #self.chat_id = self.bot.getUpdates()[-1].message.chat.id
        self.user_telegram_id = user_id

    def send_message(self, message):
        try:
            self.bot.sendMessage(chat_id=self.user_telegram_id, text=message)
        except Exception as detail:
            print(detail)

    def send_image(self, file):
        try:
            self.bot.send_photo(chat_id=self.user_telegram_id, photo=open(file, 'rb'))
        except Exception as detail:
            print(detail)

    def send_file(self, file):
        try:
            self.bot.send_document(chat_id=self.user_telegram_id, document=open(file, 'rb'))
        except Exception as detail:
            print(detail)

    def get_update_object(self):
        return self.bot.get_updates()



