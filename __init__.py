from app.database.DB import DB
from app.app import App
from config import API_TOKEN, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_CHARACTER_SET
from aiogram import types

db = DB(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_CHARACTER_SET)
app = App(db, 'localhost', 8899, API_TOKEN)


@app.dispatcher.message_handler(commands=['start'])
async def subscribe(message: types.Message):
    db.saveUser(message.from_user)
    await message.answer(
        "Мы создали данного бота, специально для Вас!!!\n"
        "Отправьте нам Ваше резюме. =)"
    )


@app.dispatcher.message_handler(commands=['send_resume'])
async def sendResume(message: types.Message):
    await message.answer("Отправьте свое резюме в формате PDF!")

@app.dispatcher.message_handler(commands=['delete_resume'])
async def deleteResume(message: types.Message):
    deleted = db.deleteResume(message.from_user.id)
    if deleted:
        await message.answer("Ваше резюме удаено!")
    else:
        await message.answer("Вы еще не отправляли резюме!")


@app.dispatcher.message_handler(content_types=['document'])
async def scan_message(msg: types.Message):
    print(f'documentID: {msg.document.file_id}')
    if msg.document.mime_type != 'application/pdf':
        await app.bot.send_message(msg.from_user.id, 'Формат файла не соответствует требованиям! Мы принимаем резюме '
                                                     'только в формате pdf')
        return

    try:
        document_id = msg.document.file_id
        file_info = await app.bot.get_file(document_id)
        fi = file_info.file_path
        name = msg.document.file_name
        fileURL = f'https://api.telegram.org/file/bot{API_TOKEN}/{fi}'
        db.saveResume(msg.from_user.id, document_id, fileURL, name)
        await app.bot.send_message(msg.from_user.id,
                                   'Спасибо за отправленное резюме! Мы свяжемся с Вами в ближайшее время!')
    except:
        await app.bot.send_message(msg.from_user.id,
                                   'Не удалось получить доступ к файлу. Отправьте новый')

@app.dispatcher.message_handler()
async def echo(message: types.Message):
    await message.answer('Выберите команду бота и следуйте инструкциям!')

if __name__ == '__main__':
    app.run()
