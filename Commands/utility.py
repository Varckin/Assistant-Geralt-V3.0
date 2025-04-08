from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from Logging.logger import get_logger
from UtilityKnife.utility import UUID, GeneratorPass
from Localization.localozation import get_str


utility_router = Router()
logger = get_logger(__name__)

@utility_router.message(Command("uuid4"))
async def cmd_uuid4(message: Message):
    gen = UUID()
    await message.reply(text=gen.create_uuid4())

@utility_router.message(Command("uuid3"))
async def cmd_uuid3(message: Message):
    try:
        _, text = message.text.split(' ', 1)
        gen = UUID()
        await message.reply(text=gen.create_uuid3(text))
    except ValueError as e:
        text = await get_str(message.from_user.id, 'error')
        await message.reply(text=text)
        logger.error(e)

@utility_router.message(Command("uuid5"))
async def cmd_uuid5(message: Message):
    try:
        _, text = message.text.split(' ', 1)
        gen = UUID()
        await message.reply(text=gen.create_uuid5(text))
    except ValueError as e:
        text = await get_str(message.from_user.id, 'error')
        await message.reply(text=text)
        logger.error(e)

@utility_router.message(Command("genpass"))
async def cmd_genpass(message: Message):
    try:
        gen = GeneratorPass()
        cmd, param, length = message.text.split(' ', 2)
        length = int(length)
        param = param.lower()

        l: bool = 'l' in param
        u: bool = 'u' in param
        d: bool = 'd' in param
        s: bool = 's' in param

        if len(param) <= 4 and (l or u or d or s):
            password: str = gen.gen_pass(length=length, use_lower=l,
                                         use_upper=u, use_digits=d,
                                         use_special=s)
            await message.reply(text=password)
        else:
            text = await get_str(message.from_user.id, 'error')
            await message.reply(text=text)
    except (ValueError, IndexError) as e:
        text = await get_str(message.from_user.id, 'error')
        await message.reply(text=text)
        logger.error(e)

@utility_router.message(Command("me"))
async def cmd_user_info(message:Message):
    text: str = f"""
Username: @{message.from_user.username}
Id: `{message.from_user.id}`
First: `{message.from_user.first_name}`
Last: `{message.from_user.last_name}`
Lang: `{message.from_user.language_code}`
"""
    await message.reply(text=text, parse_mode='MarkdownV2')
