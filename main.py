import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

API_TOKEN = '7209339260:AAEOWJsT7pXiYf2n7NYN2l_Kv1qEag6lZ4Q'
WEBAPP_URL = 'https://vladislav01192007.github.io/alt-miner-webapp/'

# Налаштування логування
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Хендлер /start
async def send_welcome(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Start farming ALT", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
    )
    # Видалити попередню клавіатуру (якщо була)
    await message.answer(
        "Welcome to ALTSETING Miner! ⛏️\nFarm $ALT and upgrade! 🔥",
        reply_markup=keyboard
    )

# Хендлер для приховування клавіатури (за бажанням)
@dp.message(F.text == "/hide")
async def hide_keyboard(message: Message):
    await message.answer("Меню приховано ✅", reply_markup=ReplyKeyboardRemove())

async def main():
    # Реєстрація хендлерів
    dp.message.register(send_welcome, F.text == "/start")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

