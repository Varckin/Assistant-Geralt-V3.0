from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from NLP.mistral7B import NLP


nlp_router = Router()

class NLPState(StatesGroup):
    NLPState = State()

@nlp_router.message(Command("nlp"))
async def cmd_nlp(message: Message, state: FSMContext):
    await state.set_state(NLPState.NLPState)
    await message.answer("Привет! Я локальный ИИ-бот на Mistral 7B. Задай мне вопрос.")

@nlp_router.message(NLPState.NLPState)
async def nlp(message: Message):
    prompt = f"[INST] {message.text} [/INST]"
    await message.answer("Думаю...")
    nlp = NLP()
    answer = await nlp.generation(prompt=prompt)
    await message.answer(answer or "Не удалось получить ответ.")
