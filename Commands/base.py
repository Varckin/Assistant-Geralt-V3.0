from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os
from Models.configDB import async_session
from sqlalchemy.future import select
from Models.models import User
from Logging.logger import get_logger
from Localization.localozation import get_str

load_dotenv()
base_router = Router()
logger = get_logger(__name__)

@base_router.message(Command("start"))
async def cmd_start(message: Message):
    try:
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.user_id == message.from_user.id)
            )
            existing_user = result.scalar_one_or_none()

            if not existing_user:                
                user = User(user_id=message.from_user.id, username=message.from_user.username,
                            first_name=message.from_user.first_name, language_code=message.from_user.language_code)
                session.add(user)
                await session.commit()
                text: str = await get_str(user_id=message.from_user.id, key_str="HelloNewUser")
                await message.answer(text=text.format(first_name=message.from_user.first_name))
            else:
                text: str = await get_str(user_id=message.from_user.id, key_str="HelloOldUser")
                await message.answer(text=text.format(first_name=message.from_user.first_name))
    except Exception as e:
        logger.error(e)

@base_router.message(Command("about"))
async def cmd_about(message: Message):
    version: str = os.getenv("VERSION_BOT")
    creator: str = os.getenv('CREATOR_BOT')
    text: str = await get_str(user_id=message.from_user.id, key_str="About")
    await message.answer(text=text.format(version=version, creator=creator),
                         parse_mode='Markdown')

@base_router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        text: str = await get_str(user_id=message.from_user.id, key_str="NoActiveState")
        await message.answer(text=text)
    else:
        await state.clear()
        text: str = await get_str(user_id=message.from_user.id, key_str="YesActiveState")
        await message.answer(text=text)
