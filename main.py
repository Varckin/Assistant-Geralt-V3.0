import asyncio, os
from Logging.logger import get_logger
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from Models.configDB import init_db

from Commands.base import base_router
from Commands.ping import ping_router
from Commands.gallows import gallows_router
from Commands.utility import utility_router
from Commands.voice import voice_router
from Commands.cert import cert_router
from Commands.admin import admin_router
from Commands.nlp import nlp_router


load_dotenv()
logger = get_logger(__name__)

async def main():
    token: str = os.getenv("BOT_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(base_router)
    dp.include_router(ping_router)
    dp.include_router(gallows_router)
    dp.include_router(utility_router)
    dp.include_router(voice_router)
    dp.include_router(cert_router)
    dp.include_router(admin_router)
    dp.include_router(nlp_router)

    await init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logger.info('Start bot')
        asyncio.run(main())
    except Exception as e:
        logger.critical(e)
