import logging
import os
import json
from aiogram import Bot, Dispatcher, types, executor

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен и admin username из переменных среды
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "@your_username")

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Загрузка каталога из JSON
def load_catalog():
    with open("catalog.json", encoding="utf-8") as f:
        return json.load(f)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🪴 Каталог", "📦 Оформить заказ")
    keyboard.add("🚚 Доставка", "📞 Связь с продавцом")
    await message.answer("Привет! Это бот-магазин растений 🌿", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text == "🪴 Каталог")
async def show_catalog(message: types.Message):
    catalog = load_catalog()
    for item in catalog:
        text = f"**{item['name']}**\nЦена: {item['price']}\n{item['description']}"
        photo = item["photo"]
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, parse_mode="Markdown")

@dp.message_handler(lambda msg: msg.text == "📦 Оформить заказ")
async def order_request(message: types.Message):
    await message.reply("Напишите, пожалуйста, в одном сообщении:\n\n1. ФИО\n2. Адрес\n3. Телефон или Telegram\n4. Название растения\n5. Комментарий (если есть)")

@dp.message_handler(lambda msg: msg.text == "🚚 Доставка")
async def show_shipping(message: types.Message):
    await message.reply("Мы доставляем по России и СНГ. Оплата — переводом. Подробности в чате с продавцом.")

@dp.message_handler(lambda msg: msg.text == "📞 Связь с продавцом")
async def contact_seller(message: types.Message):
    await message.reply(f"Связаться с продавцом: {ADMIN_USERNAME}")

# Любое другое сообщение → переслать админу
@dp.message_handler()
async def forward_order(message: types.Message):
    await message.reply("Спасибо! Мы получили ваше сообщение — свяжемся с вами скоро 🌱")
    await bot.send_message(chat_id=ADMIN_USERNAME, text=f"📬 Новое сообщение от @{message.from_user.username}:\n\n{message.text}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
