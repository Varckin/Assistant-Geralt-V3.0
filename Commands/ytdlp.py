from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from Logging.logger import get_logger
from Localization.localozation import get_str
from YtDLP.youtube import Youtube

ytdlp_router = Router()
logger = get_logger(__name__)


class ytdlp_State(StatesGroup):
    YoutubeMusicState = State()


@ytdlp_router.message(Command("youtube"))
async def youtube_cmd(message: Message, state: FSMContext):
    await state.set_state(ytdlp_State.YoutubeMusicState)
    text = await get_str(user_id=message.from_user.id,
                         key_str='helloYoutube')
    await message.reply(text=text)

@ytdlp_router.message(ytdlp_State.YoutubeMusicState)
async def download(message: Message):
    ytb = Youtube()
    text = await get_str(user_id=message.from_user.id,
                         key_str='downloadYoutube')
    await message.reply(text=text)
    
    await ytb.download_audio(url=message.text, message=message)
