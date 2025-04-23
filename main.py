import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

API_TOKEN = '7209339260:AAEueuoTmhTNviLRlC8MrrekT5r7CM7NWMA'
WEBAPP_URL = 'https://vladislav01192007.github.io/alt-miner-webapp/'
            
# Налаштування логування
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Хендлер окремо, без декоратора
async def send_welcome(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀 Start farming ALT", web_app=WebAppInfo(url=WEBAPP_URL))
            ]
        ]
    )
    await message.answer("Welcome to ALTSETING Miner! ⛏️\nFarm $ALT and upgrade! 🔥", reply_markup=keyboard)

async def main():
    # ✅ Реєструємо хендлер вручну
    dp.message.register(send_welcome, F.text == "/start")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
