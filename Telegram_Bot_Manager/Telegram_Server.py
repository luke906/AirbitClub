from Telegram_Class import Telegram_Manager

if __name__ == "__main__":

    Telegram_Mng = Telegram_Manager()
    updates = Telegram_Mng.get_update_object()
    for u in updates:
        print(u.message)
