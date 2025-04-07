from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from Logging.logger import get_logger
from Localization.localozation import get_str
from uuid import uuid4
from pathlib import Path
from Voice.STT import STT
from Voice.TTS import TTS


voice_router = Router()
logger = get_logger(__name__)
LANGUAGES: dict = {
    "🇷🇺 Русский": "ru",
    "🇺🇸 English": "en",
    "🇩🇪 Deutsch": "de",
    "🇪🇸 Español": "es",
    "🇫🇷 Français": "fr"
}

class TTS_STT_State(StatesGroup):
    STTState = State()

    TTSChoosingLangState = State()
    TTSState = State()

@voice_router.message(Command("stt"))
async def cmd_stt(message: Message, state: FSMContext):
    await state.set_state(TTS_STT_State.STTState)
    text = await get_str(message.from_user.id, 'STTSend')
    await message.reply(text=text)

@voice_router.message(TTS_STT_State.STTState)
async def stt_voice(message: Message):
    try:
        stt = STT()
        TMP_DIR = Path('tmp')
        TMP_DIR.mkdir(exist_ok=True)
        name_file = uuid4().hex
        source_path = TMP_DIR / f"STT_{name_file}.ogg"
        destination_path = TMP_DIR / f"STT_{name_file}.wav"

        voice = message.voice
        file_info = await message.bot.get_file(voice.file_id)
        file_path = file_info.file_path
        await message.bot.download_file(file_path, source_path)

        text = await get_str(message.from_user.id, 'GenerationAI')
        await message.answer(text=text)
        text, language = stt.convert_voice_to_text(source_path, destination_path)
        text_send = await get_str(message.from_user.id, 'STTRecongnized')
        await message.reply(text_send.format(text=text, language=language))
    except Exception as e:
        logger.error(e)

@voice_router.message(Command("tts"))
async def cmd_tts(message: Message, state: FSMContext):
    list_btn = [KeyboardButton(text=label) for label in LANGUAGES.keys()]

    kb = ReplyKeyboardMarkup(
        keyboard=[list_btn[i:i + 3] for i in range(0, len(list_btn), 3)], resize_keyboard=True, one_time_keyboard=True
    )

    await state.set_state(TTS_STT_State.TTSChoosingLangState)
    text = await get_str(message.from_user.id, 'TTSChooseLang')
    await message.reply(text=text, reply_markup=kb)

@voice_router.message(TTS_STT_State.TTSChoosingLangState)
async def tts_choosing_lang(message: Message, state: FSMContext):
    lang_code = LANGUAGES.get(message.text)
    if lang_code is None:
        text = await get_str(message.from_user.id, 'TTSNotSupLang')
        await message.reply(text)
        return
    
    await state.update_data(lang=lang_code)
    await state.set_state(TTS_STT_State.TTSState)
    text = await get_str(message.from_user.id, 'TTSSend')
    await message.reply(text=text, reply_markup=ReplyKeyboardRemove())

@voice_router.message(TTS_STT_State.TTSState)
async def tts_text(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()
        lang = user_data.get('lang')
        tts = TTS()
        text = await get_str(message.from_user.id, 'GenerationAI')
        await message.answer(text=text)
        await message.reply_voice(voice=FSInputFile(tts.convert_text_to_voice(text=message.text, lang=lang)))
    except Exception as e:
        logger.error(e)
