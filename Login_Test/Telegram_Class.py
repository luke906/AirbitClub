
import telegram

class Telegram_Manager:

    def __init__(self):
        self.bot = telegram.Bot(token='453642591:AAFwBdO7CaZ4XpfYi1ud3b6nURjYisHgs-s')
        self.updates = self.bot.getUpdates()  # 업데이트 내역을 받아옵니다.
        # self.chat_id = self.bot.getUpdates()[-1].message.chat.id

    def send_message(self, message):
        self.bot.sendMessage(chat_id='468017156', text=message)
