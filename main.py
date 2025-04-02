import asyncio, os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from Commands.base import base_router


load_dotenv()

async def main():
    token: str = os.getenv("BOT_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(base_router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
