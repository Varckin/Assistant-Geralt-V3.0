from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from PingService.pingService import PingService


ping_router = Router()

@ping_router.message(Command("ping"))
async def cmd_ping(message: Message):
    try:
        _, url = message.text.split(' ', 1)
        ping = PingService(url)
        await message.reply(text=ping.ping())
    except ValueError:
        await message.reply('Error, Use: <cmd> <URL>')
