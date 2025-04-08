from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from Logging.logger import get_logger
from Localization.localozation import get_str
from Admin.admin import AdminPanel


logger = get_logger(__name__)
admin_router = Router()

@admin_router.message(Command("intusers"))
async def cmd_int_users(message: Message):
    admin_panel = AdminPanel()

    if admin_panel.check_admin_id(message.from_user.id):
        text = await admin_panel.how_many_users_total()
        await message.reply(text)

@admin_router.message(Command("allusers"))
async def cmd_all_users(message: Message):
    admin_panel = AdminPanel()

    if admin_panel.check_admin_id(message.from_user.id):
        text = await admin_panel.show_all_users()
        await message.reply(text, parse_mode='MarkdownV2')
