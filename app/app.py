from threading import Thread
from app.utils.WaitGroup import WaitGroup
from aiogram import Bot, Dispatcher, executor


class App:
    def __init__(self, db, host, port, bot_token):
        self.__wg = WaitGroup()
        self.__db = db
        self.__server_address = (host, port)
        self.bot = Bot(token=bot_token)
        self.dispatcher = Dispatcher(self.bot)

    def run(self):
        Thread(target=self.__runBot()).start()
        # add new corutine
        self.__wg.wait()
        print("BEFORE APP FINISHING")

    def __runBot(self):
        print("START BOT")
        self.__wg.add()
        executor.start_polling(dispatcher=self.dispatcher, skip_updates=True)
        print("BOT STOPPING")
        self.__wg.done()

