from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from Logging.logger import get_logger
from Localization.localozation import get_str
from YtDLP.celery_tasks import download_soundcloud, download_youtube

ytdlp_router = Router()
logger = get_logger(__name__)


class ytdlp_State(StatesGroup):
    YoutubeMusicState = State()
    SoundclodMusicState = State()


@ytdlp_router.message(Command("youtube"))
async def youtube_cmd(message: Message, state: FSMContext):
    await state.set_state(ytdlp_State.YoutubeMusicState)
    text = await get_str(user_id=message.from_user.id,
                         key_str='helloYoutube')
    await message.reply(text=text)

@ytdlp_router.message(ytdlp_State.YoutubeMusicState)
async def download_youtube(message: Message):
    text = await get_str(user_id=message.from_user.id,
                         key_str='downloadYoutube')
    await message.reply(text=text)

    download_youtube.delay(message.text, message.chat.id)

@ytdlp_router.message(Command("soundcloud"))
async def youtube_cmd(message: Message, state: FSMContext):
    await state.set_state(ytdlp_State.SoundclodMusicState)
    text = await get_str(user_id=message.from_user.id,
                         key_str='helloYoutube')
    await message.reply(text=text)

@ytdlp_router.message(ytdlp_State.SoundclodMusicState)
async def download_youtube(message: Message):
    text = await get_str(user_id=message.from_user.id,
                         key_str='downloadYoutube')
    await message.reply(text=text)

    download_soundcloud.delay(message.text, message.chat.id)