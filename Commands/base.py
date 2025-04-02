from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import os



load_dotenv()
base_router = Router()

@base_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(text=f"Hello {message.chat.first_name}")

@base_router.message(Command("about"))
async def cmd_about(message: Message):
    version: str = os.getenv("VERSION_BOT")
    creator: str = os.getenv('CREATOR_BOT')
    
    await message.answer(text=f"Creator: {creator}\nVersion: {version}",
                         parse_mode='Markdown')
