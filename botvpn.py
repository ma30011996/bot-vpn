from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("🔥 Получить VPN"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n\n"
        "Этот бот выдаёт быстрый и надёжный VPN.\n"
        "Нажми кнопку ниже, чтобы получить доступ.",
        reply_markup=menu
    )

@dp.message_handler(lambda message: message.text == "🔥 Получить VPN")
async def get_key(message: types.Message):
    try:
        with open("keys.txt", "r") as f:
            keys = f.readlines()

        if not keys:
            await message.answer("Ключи закончились. Попробуй позже.")
            return

        key = keys[0].strip()
        with open("keys.txt", "w") as f:
            f.writelines(keys[1:])

        await message.answer(f"✅ Вот твой ключ:\n`{key}`", parse_mode="Markdown")
    except Exception as e:
        await message.answer("Произошла ошибка.")
        print("Ошибка:", e)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)