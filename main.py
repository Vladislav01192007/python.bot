import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

API_TOKEN = '7209339260:AAE8jh5r-qRyUQiTDsd8wtQaCUYWohWcxbk'
WEBAPP_URL = 'https://vladislav01192007.github.io/alt-miner-webapp/'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = 'https://https://python-bot-1-33f9.onrender.com.onrender.com' + WEBHOOK_PATH

# Налаштування логування
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Хендлер /start
@dp.message(F.text == "/start")
async def send_welcome(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Start farming ALT", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
    )
    await message.answer(
        "Welcome to ALTSETING Miner! ⛏️\nFarm $ALT and upgrade! 🔥",
        reply_markup=keyboard
    )

# Хендлер приховування клавіатури
@dp.message(F.text == "/hide")
async def hide_keyboard(message: Message):
    await message.answer("Меню приховано ✅", reply_markup=ReplyKeyboardRemove())

# ===== Webhook сервер =====
async def handle_webhook(request):
    update = await request.json()
    await dp.feed_update(bot, update)
    return web.Response()

async def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    await bot.set_webhook(WEBHOOK_URL)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)  # Порт 10000 для Render
    await site.start()

    logging.info(f"Webhook listening on {WEBHOOK_URL}")

    # Безкінечний цикл
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
