import asyncio, logging, sqlite3, time
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command 
from config import token

bot=Bot(token=token)
dp=Dispatcher()
logging.basicConfig(level=logging.INFO)

connection=sqlite3.connect('tasks.db')
cursor=connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               task TEXT)""")
order_data={}

@dp.message(Command('start'))
async def start(message:Message):
    await message.answer(f'Привет! Я бот для управление задачами.  Используй команду /add, чтобы добавить задачу, /view — чтобы посмотреть все задачи, и /delete — чтобы удалить задачу')

@dp.message(Command('add'))
async def add_tasks(message:Message):             # ? - плейсхолдер (заместитель) 
    cursor.execute("SELECT task FROM tasks WHERE user_id = ?", message.from_user.id,)    
    tasks = cursor.fetchall()
    if tasks:
        response = '\n'.join([task[0] for task in tasks]) 
    else:
        response = "У вас нет заметок."
    await message.answer(response)

# @dp.message(Command('add1'))
# async def save_tasks(message:Message):
#     cursor.execute('INSERT INTO tasks (user_id, task) VALUES (?, ?)', (message.from_user.id, message.text))
#     connection.commit()
#     await message.answer("Заметка сохранена!")
    
    
    
    # cursor.execute('INSERT INTO tasks (id, user_id, task) VALUES (?, ?, ?)', (message.message_id, message.from_user.id, message.text))
    # connection.commit()
    # await message.answer("Задача сохранена!")





async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())