import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from config import token, chat_id
from main import check_new_work, get_all_work, check_work_status

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dt = Dispatcher(bot)


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
