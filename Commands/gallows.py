from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from Gallows.gallows import Gallows
from Logging.logger import get_logger
from Localization.localozation import get_str


logger = get_logger(__name__)
gallows_router = Router()

class GallowsState(StatesGroup):
    gallowsState = State()


@gallows_router.message(Command("gallows"))
async def cmd_gallows(message: Message, state: FSMContext):
    gall = Gallows()
    tries: int = gall.tries
    selected_word: str = gall.choice_word()
    guessed_letters: list = []
    guessed_word: str = ''.join('*' if letter not in guessed_letters else letter for letter in selected_word)

    await state.update_data(
        selected_word=selected_word,
        guessed_word=guessed_word,
        guessed_letters=guessed_letters,
        tries=tries
    )
    await state.set_state(GallowsState.gallowsState)
    text: str = await get_str(user_id=message.from_user.id, key_str="gallowWordSelected")
    await message.answer(text=text.format(guessed_word=guessed_word, tries=tries))


@gallows_router.message(GallowsState.gallowsState)
async def game_run(message: Message, state: FSMContext):
    gall = Gallows()
    data: dict = await state.get_data()
    selected_word: str = data['selected_word']
    guessed_letters: list = data['guessed_letters']
    guessed_word: str = data['guessed_word']
    tries: int = data['tries']

    guess = message.text.lower()
    try:
        if len(guess) != 1:
            text: str = await get_str(user_id=message.from_user.id, key_str="gallowEnterOneLetter")
            await message.reply(text=text.format(guessed_word=guessed_word))
            return

        if guess in guessed_letters:
            text: str = await get_str(user_id=message.from_user.id, key_str="gallowAlreadyLetter")
            await message.reply(text=text.format(guessed_word=guessed_word))
            return
        
        if guess in selected_word:
            guessed_letters.append(guess)
            guessed_word = ''.join(letter if letter in guessed_letters else '*' for letter in selected_word)

            if guessed_word == selected_word:
                text: str = await get_str(user_id=message.from_user.id, key_str="gallowCongratulation")
                await message.reply(text=text.format(guessed_word=guessed_word))
                await state.clear()
            else:
                text: str = await get_str(user_id=message.from_user.id, key_str="gallowRight")
                await message.reply(text=text.format(guessed_word=guessed_word))
        else:
            tries -= 1

            if tries == 0:
                text: str = await get_str(user_id=message.from_user.id, key_str="gallowLost")
                await message.reply(text=text.format(selected_word=selected_word))
                gif = FSInputFile(gall.gif_load())
                await message.answer_animation(animation=gif)
                await state.clear()
            else:
                text: str = await get_str(user_id=message.from_user.id, key_str="gallowWrong")
                await message.reply(text=text.format(guessed_word=guessed_word, tries=tries))

        await state.update_data(
            guessed_word=guessed_word,
            guessed_letters=guessed_letters,
            tries=tries
        )
    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
    except PermissionError as e:
        logger.error(f'No permission: {e}')
    except Exception as e:
        logger.error(f'Error: {e}')
