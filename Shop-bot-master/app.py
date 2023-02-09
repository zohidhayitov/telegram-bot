import os
import handlers
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import config
from loader import dp, db, bot
import filters
import logging

filters.setup(dp)

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))
user_message = 'Foydalanuvchi'
admin_message = 'Admin'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(user_message, admin_message)

    await message.answer('''Salom! 👋

🤖 Men har qanday toifadagi tovarlarni sotadigan bot-do'konman.
    
🛍️ Katalogga o'tish va o'zingizga yoqqan mahsulotlarni tanlash uchun /menu buyrug'idan foydalaning.

💰 Hisobingizni Humo, Uzcard yoki Visa orqali to'ldirishingiz mumkin.

❓ Savollaringiz bormi? Muammo bormi?! /sos buyrug'i sizga imkon qadar tezroq javob berishga harakat qiladigan administratorlar bilan bog'lanishga yordam beradi.

🤝 Shu kabi botga buyurtma berasizmi? Ishlab chiquvchi <a href="https://t.me/zohid_shoberdiyevich">Zohid Hayitov</a> bilan bog'laning, u sizga qo'lidan kelganicha ko'mak beradi.)))
    ''', reply_markup=markup)


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):

    cid = message.chat.id
    if cid in config.ADMINS:
        config.ADMINS.remove(cid)

    await message.answer('Foydalanuvchi rejimi yoqilgan.', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):

    cid = message.chat.id
    if cid not in config.ADMINS:
        config.ADMINS.append(cid)

    await message.answer('Administrator rejimi yoqilgan.', reply_markup=ReplyKeyboardRemove())


async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()

    await bot.delete_webhook()
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown():
    logging.warning("Oʻchirish..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Pastga")


if __name__ == '__main__':

    if "HEROKU" in list(os.environ.keys()):

        executor.start_webhook(
            dispatcher=dp,
            webhook_path=config.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )

    else:

        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
