import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

API_TOKEN = '7646902024:AAHyk78PJU5ulvUs2Nc48Qz7gcwM2EUOOsg'
WEBAPP_URL = 'https://vladislav01192007.github.io/alt-miner-webapp/'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = 'https://python-bot-1-33f9.onrender.com' + WEBHOOK_PATH

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
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return web.Response()

async def main():
    # Створюємо aiohttp веб-сервер
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    # Встановлюємо webhook
    await bot.set_webhook(WEBHOOK_URL)

    # Запускаємо сервер на порту 10000 (Render специфіка)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

    logging.info(f"Webhook listening on {WEBHOOK_URL}")

    # Тримаємо процес живим
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
