import os
import random
import string
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

waiting = {}

def generate_password():
    length = random.randint(10, 18)
    chars = string.ascii_letters + string.digits + "!@#$%^&*_-"
    return ''.join(random.choice(chars) for _ in range(length))

@dp.message(CommandStart())
async def start(message: Message):
    waiting[message.from_user.id] = 1
    await message.answer("Привет! Напиши ник своего обидчика 😈")

@dp.message(F.text)
async def handle(message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    if user_id not in waiting:
        waiting[user_id] = 1
        await message.answer("Привет! Напиши ник своего обидчика 😈")
        return

    if waiting[user_id] == 1:
        waiting[user_id] = 2
        await message.answer("Теперь напиши сервер, где он играет")
    elif waiting[user_id] == 2:
        password = generate_password()
        await message.answer(
            f"Готово! Взломал аккаунт <b>{text}</b>\n\n"
            f"Пароль: <code>{password}</code>\n"
            f"Заходи и мсти)",
            parse_mode="HTML"
        )
        del waiting[user_id]

async def main():
    print("Тролль-бот запущен и ждёт жертв 😈")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
