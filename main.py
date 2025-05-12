import asyncio
import logging
import json
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# === Конфігурація ===
API_TOKEN = '7646902024:AAHyk78PJU5ulvUs2Nc48Qz7gcwM2EUOOsg'
WEBAPP_URL = 'https://vladislav01192007.github.io/alt-miner-webapp/'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = 'https://python-bot-1-33f9.onrender.com' + WEBHOOK_PATH
DATA_FILE = "user_data.json"

# === Логування ===
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# === Робота з JSON (ALT баланс) ===
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def update_user_alt(user_id: int, amount: int):
    data = load_data()
    user_id_str = str(user_id)
    data[user_id_str] = data.get(user_id_str, 0) + amount
    save_data(data)
    return data[user_id_str]

# === Хендлери ===
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

@dp.message(F.text == "/hide")
async def hide_keyboard(message: Message):
    await message.answer("Меню приховано ✅", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "/ref")
async def referral_link(message: Message):
    bot_user = await bot.get_me()
    username = bot_user.username
    user_id = message.from_user.id
    ref_link = f"https://t.me/{username}?start={user_id}"
    await message.answer(f"🎁 Запроси друзів та отримай ALT!\nОсь твоє посилання:\n<code>{ref_link}</code>")

@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    try:
        alt = int(message.web_app_data.data)
        update_user_alt(message.from_user.id, alt)
        # Тихо оброблюємо ALT
    except Exception as e:
        logging.error(f"❌ Помилка обробки ALT: {e}")

# === Webhook сервер ===
async def handle_webhook(request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return web.Response()

async def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    await bot.set_webhook(WEBHOOK_URL)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    logging.info(f"Webhook listening on {WEBHOOK_URL}")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
