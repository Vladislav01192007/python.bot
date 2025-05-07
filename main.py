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

def convert_alt_to_altst(user_id: int):
    data = load_data()
    user_id_str = str(user_id)
    alt = data.get(user_id_str, 0)
    if alt < 10:
        return (False, alt)
    altst = alt // 10
    data[user_id_str] = alt % 10
    save_data(data)
    return (True, altst)

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

@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    try:
        alt = int(message.web_app_data.data)
        total = update_user_alt(message.from_user.id, alt)
        await message.answer(f"✅ Ви надіслали <b>{alt}</b> ALT!\n🔄 Загальний баланс: <b>{total}</b> ALT")
    except Exception as e:
        await message.answer(f"❌ Помилка: {e}")

@dp.message(F.text == "/wallet")
async def wallet_handler(message: Message):
    data = load_data()
    user_id_str = str(message.from_user.id)
    alt = data.get(user_id_str, 0)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💱 Обміняти ALT → ALTST", callback_data="convert_alt")]
        ]
    )

    await message.answer(
        f"👛 <b>Ваш гаманець</b>\n🔹 ALT: <b>{alt}</b>\n🔸 ALTST: натисніть кнопку нижче для обміну",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "convert_alt")
async def convert_callback(callback):
    user_id = callback.from_user.id
    success, result = convert_alt_to_altst(user_id)
    if success:
        await callback.message.edit_text(
            f"✅ Ви обміняли ALT на <b>{result} ALTST</b>!\nРешта ALT: <b>{load_data().get(str(user_id), 0)}</b>"
        )
    else:
        await callback.answer("❌ Потрібно мінімум 10 ALT для обміну!", show_alert=True)

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
