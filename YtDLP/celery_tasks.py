from celery_conf import celery_app
from aiogram import Bot
from aiogram.types import FSInputFile
from .youtube import Youtube
import os
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")

@celery_app.task
def download_and_send(url: str, chat_id: int):
    youtube = Youtube()
    new_files = youtube.download_audio(url)

    asyncio.run(send_files(new_files, chat_id))

async def send_files(files, chat_id):
    bot = Bot(token=BOT_TOKEN)

    for path in files:
        try:
            await bot.send_audio(chat_id=chat_id, audio=FSInputFile(path))
            await asyncio.sleep(5)
        except Exception as e:
            await bot.send_message(chat_id=chat_id, text=f"Error sending {path.name}: {e}")
        finally:
            try:
                path.unlink()
            except Exception as e:
                print(f"Failed to delete {path}: {e}")

    await bot.session.close()
