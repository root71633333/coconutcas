import logging
import sqlite3
import random
import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import WebAppInfo, LabeledPrice, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
API_TOKEN = '7546865748:AAE32kq2bPOeUzD84sdTHOYVa4-em0Pz6oQ'
WEBAPP_URL = 'https://core.telegram.org/bots/coconutcas'
DB_NAME = 'casino.db'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Инициализация БД
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    balance REAL DEFAULT 0,
    referrer_id INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    type TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()


def get_main_keyboard():
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.KeyboardButton(
            text="🎰 Открыть Казино",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )  # Закрываем KeyboardButton
    )  # Закрываем метод add


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    referrer = message.get_args()
    user_id = message.from_user.id

    cursor.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)",
                   (user_id, message.from_user.username))

    if referrer and referrer.isdigit():
        cursor.execute("UPDATE users SET referrer_id = ? WHERE id = ?",
                       (int(referrer), user_id))

    conn.commit()
    await message.answer(
        "🏝 Добро пожаловать в Coconut Casino!\n"
        "Нажмите кнопку ниже, чтобы начать играть!",
        reply_markup=get_main_keyboard()
    )


@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        user_id = message.from_user.id

        # Получаем текущий баланс
        cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
        balance = cursor.fetchone()[0]

        # Обработка игры
        if data['game_type'] == 'coin_flip':
            bet = float(data['bet'])
            choice = data['choice']

            if bet > balance:
                return await message.answer("❌ Недостаточно средств!")

            result = random.choice(['heads', 'tails'])
            if choice == result:
                win_amount = bet * 1.95
                new_balance = balance - bet + win_amount
                await message.answer(
                    f"🎉 Победа! Выпало {result}\n"
                    f"💵 Выигрыш: ${win_amount:.2f}\n"
                    f"💰 Новый баланс: ${new_balance:.2f}"
                )
            else:
                new_balance = balance - bet
                await message.answer(
                    f"💥 Проигрыш! Выпало {result}\n"
                    f"💰 Новый баланс: ${new_balance:.2f}"
                )

            # Обновляем баланс
            cursor.execute("UPDATE users SET balance = ? WHERE id = ?",
                           (new_balance, user_id))
            conn.commit()

    except Exception as e:
        logger.error(f"WebApp error: {e}")
        await message.answer("⚠ Произошла ошибка при обработке запроса")


@dp.message_handler(commands=['deposit'])
async def cmd_deposit(message: types.Message):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Пополнение баланса USDT",
        description="Пополнение через Telegram Payments",
        payload="deposit",
        provider_token="ВАШ_ПЛАТЕЖНЫЙ_ТОКЕН",
        currency="USD",
        prices=[LabeledPrice(label="USDT", amount=10000)],  # 100.00 USD
        start_parameter="deposit"
    )


@dp.pre_checkout_query_handler()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_payment(message: types.Message):
    user_id = message.from_user.id
    amount = message.successful_payment.total_amount / 100  # Конвертация в USD

    cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?",
                   (amount, user_id))
    conn.commit()

    await message.answer(f"✅ Баланс успешно пополнен на ${amount:.2f}")

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def handle_web_app(message: types.Message):
    data = json.loads(message.web_app_data.data)
    await message.answer(f"Получены данные: {data}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)