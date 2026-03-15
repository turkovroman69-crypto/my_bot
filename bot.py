import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# ==== ТВОИ ДАННЫЕ (ВСТАВЬ СЮДА) ====
BOT_TOKEN = "8669143845:AAGGmF8Sclww-FhOBBBIMo2c2ij171XQi0c"
CHANNEL_LINK = "https://t.me/+gCGSbbXViGkxNzcy"
SUB_PRICE = 1
# ===================================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Это платный канал.\n"
        f"💰 Цена: {SUB_PRICE} ⭐ (Telegram Stars).\n"
        "Нажми кнопку для оплаты.",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=f"Оплатить {SUB_PRICE} ⭐", callback_data="buy")]
        ])
    )

@dp.callback_query(lambda c: c.data == 'buy')
async def process_buy(callback: types.CallbackQuery):
    prices = [types.LabeledPrice(label="Подписка", amount=SUB_PRICE)]
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Доступ к каналу",
        description="Доступ на 30 дней.",
        payload="sub-payload",
        provider_token="",
        currency="XTR",
        prices=prices,
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="✅ Оплатить", pay=True)]
        ])
    )
    await callback.answer()

@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message(lambda message: message.successful_payment is not None)
async def successful_payment(message: Message):
    await message.answer(
        f"✅ Оплата прошла!\n"
        f"🔗 Вот ссылка на канал: {CHANNEL_LINK}\n"
        "Если не заходит, напиши @твой_логин"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())