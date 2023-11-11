import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from config import token, chat_id
from main import check_new_work, get_all_work, check_work_status

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dt = Dispatcher(bot)

user_id = "157410552", '727996273', '190586788', '1156981100'
chat_id_required = user_id


@dt.message_handler(commands="start", user_id=chat_id_required)
async def start(message: types.Message):
    await message.reply("Введите пароль")


@dt.message_handler(text="C0442474040", user_id=chat_id_required)
async def password(message: types.Message):
    start_buttons = ["Последние 20", "Последние 10", "Новые", "Мар'ян", "Славик"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.reply("Пивет! Удачного дня)", reply_markup=keyboard)


@dt.message_handler(Text(equals="Последние 20"), user_id=chat_id_required)
async def get_work(message: types.Message):
    with open("work_dict.json") as file:
        work_dict = json.load(file)

    for k, v in sorted(work_dict.items())[-20:]:
        work = (f"<b>ИД:</b> {v['work_ID']}\n"
                f"<b>Тема:</b> {v['work_iss']}\n"
                f"<b>Описание:</b> {v['work_iss_des']}\n"
                f"<b>Юзер:</b> {v['work_user']}\n"
                f"<b>Контакты:</b> {v['work_phone']}\n"
                f"<b>Адрес:</b> {v['work_adr']}\n"
                f"<b>Cтатус:</b> {v['work_status']}\n")

        await message.answer(work)


@dt.message_handler(Text(equals="Последние 10"), user_id=chat_id_required)
async def get_last_ten_work(message: types.Message):
    with open("work_dict.json") as file:
        work_dict = json.load(file)
    for k, v in sorted(work_dict.items())[-10:]:
        work = (f"<b>ИД:</b> {v['work_ID']}\n"
                f"<b>Тема:</b> {v['work_iss']}\n"
                f"<b>Описание:</b> {v['work_iss_des']}\n"
                f"<b>Юзер:</b> {v['work_user']}\n"
                f"<b>Контакты:</b> {v['work_phone']}\n"
                f"<b>Адрес:</b> {v['work_adr']}\n"
                f"<b>Cтатус:</b> {v['work_status']}\n")

        await message.answer(work)


@dt.message_handler(Text(equals="Новые"), user_id=chat_id_required)
async def get_new_work(message: types.Message):
    work_status = check_work_status()
    for k, v in sorted(work_status.items()):
        if v['work_status'] == "новая":
            work = (f"<b>ИД:</b> {v['work_ID']}\n"
                    f"<b>Тема:</b> {v['work_iss']}\n"
                    f"<b>Описание:</b> {v['work_iss_des']}\n"
                    f"<b>Юзер:</b> {v['work_user']}\n"
                    f"<b>Контакты:</b> {v['work_phone']}\n"
                    f"<b>Адрес:</b> {v['work_adr']}\n"
                    f"<b>Cтатус:</b> {v['work_status']}\n")

            await message.answer(work)


@dt.message_handler(Text(equals="Славик"), user_id=chat_id_required)
async def get_work_status(message: types.Message):
    work_status = check_work_status()
    for k, v in sorted(work_status.items()):
        if v['work_status'] == "назначена (Яма Святослав Олегович)":
            work = (f"<b>ИД:</b> {v['work_ID']}\n"
                    f"<b>Тема:</b> {v['work_iss']}\n"
                    f"<b>Описание:</b> {v['work_iss_des']}\n"
                    f"<b>Юзер:</b> {v['work_user']}\n"
                    f"<b>Контакты:</b> {v['work_phone']}\n"
                    f"<b>Адрес:</b> {v['work_adr']}\n"
                    f"<b>Cтатус:</b> {v['work_status']}\n")

            await message.answer(work)


@dt.message_handler(Text(equals="Мар'ян"), user_id=chat_id_required)
async def get_work_status_mar(message: types.Message):
    work_status = check_work_status()
    for k, v in sorted(work_status.items()):
        if v['work_status'] == "назначена (Паньків Мар'ян Ігорович)":
            work = (f"<b>ИД:</b> {v['work_ID']}\n"
                    f"<b>Тема:</b> {v['work_iss']}\n"
                    f"<b>Описание:</b> {v['work_iss_des']}\n"
                    f"<b>Юзер:</b> {v['work_user']}\n"
                    f"<b>Контакты:</b> {v['work_phone']}\n"
                    f"<b>Адрес:</b> {v['work_adr']}\n"
                    f"<b>Cтатус:</b> {v['work_status']}\n")

            await message.answer(work)


async def get_update_every_3minute():
    while True:
        try:
            new_work = check_new_work()
            if len(new_work) >= 1:
                for k, v in sorted(new_work.items()):
                    bug_num_id = v['work_ID']
                    work = (
                        f"<b>ИД:</b> {v['work_ID']}\n"
                        f"<b>Создатель:</b> {v['work_sender']}\n"
                        f"<b>Тема:</b> {v['work_iss']}\n"
                        f"<b>Описание:</b> {v['work_iss_des']}\n"
                        f"<b>Юзер:</b> {v['work_user']}\n"
                        f"<b>Адрес:</b> {v['work_adr']}\n"
                        f"<b>Контакты:</b> {v['work_phone']}\n"
                    )
                    await bot.send_message(chat_id, work)
            await asyncio.sleep(90)
        except Exception as e:
            logging.exception("Потеря связи: %s", str(e))
            await asyncio.sleep(40)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(get_update_every_3minute())
    executor.start_polling(dt, skip_updates=True)
