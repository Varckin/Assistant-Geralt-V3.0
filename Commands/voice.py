from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from Logging.logger import get_logger
from uuid import uuid4
from pathlib import Path
from Voice.STT import STT


voice_router = Router()
logger = get_logger(__name__)

class STTState(StatesGroup):
    STTState = State()

@voice_router.message(Command("stt"))
async def cmd_stt(message: Message, state: FSMContext):
    await state.set_state(STTState.STTState)
    await message.reply(text="Send me voice....")

@voice_router.message(STTState.STTState)
async def voice(message: Message):
    try:
        stt = STT()
        TMP_DIR = Path('tmp')
        TMP_DIR.mkdir(exist_ok=True)
        name_file = str(uuid4())
        source_path = TMP_DIR / f"{name_file}.ogg"
        destination_path = TMP_DIR / f"{name_file}.wav"

        voice = message.voice
        file_info = await message.bot.get_file(voice.file_id)
        file_path = file_info.file_path
        await message.bot.download_file(file_path, source_path)

        text, language = stt.convert_voice_to_text(source_path, destination_path)
        await message.answer(f"Recognized text:{text}\nLanguage: {language}")
    except Exception as e:
        logger.error(e)
