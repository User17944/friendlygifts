from aiohttp import web
import os
import asyncio, json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
import os

# Токен берется из настроек Render (переменные окружения)
BOT_TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬТЕ_ТОКЕН_СЮДА_ЕСЛИ_ТЕСТИРУЕТЕ_ЛОКАЛЬНО")
WEB_APP_URL = "https://user17944.github.io/friendlygifts/"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Открыть магазин", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer(
        f"👋 Добро пожаловать в <b>Frendly Gifts</b>, {message.from_user.first_name}!\n\n"
        "Нажми на кнопку ниже, чтобы открыть меню покупок.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(F.web_app_data)
async def web_app_handler(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
        action = data.get('action')
        item = data.get('item')
        if action == 'buy':
            if item == 'stars':
                await message.answer("⭐ Вы выбрали покупку звёзд. Скоро тут будет выбор количества.")
            elif item == 'premium':
                await message.answer("💎 Вы выбрали покупку Premium.")
            elif item == 'nft':
                await message.answer("🗂 Вы выбрали раздел NFT.")
        elif action == 'profile':
            await message.answer(f"👤 Ваш ID: <code>{message.from_user.id}</code>", parse_mode="HTML")
    except Exception as e:
        print(f"Ошибка: {e}")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

async def web_server():
    app = web.Application()
    app.router.add_get('/', lambda r: web.Response(text="Bot is running!"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    print("Веб-сервер запущен для Render!")

async def main_wrapper():
    # Запускаем и веб-сервер для портов, и самого бота
    await asyncio.gather(
        web_server(),
        main()
    )

if __name__ == "__main__":
    asyncio.run(main_wrapper())
