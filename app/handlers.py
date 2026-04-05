from service import TaskService

from aiogram import  F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from service import TaskService
from texts import TEXT_START

router = Router()

class AddTask(StatesGroup):
    title = State()
    description = State()
    priority = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        TEXT_START,
        reply_markup=kb.main,
    )

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Команда help сработала')

@router.message(F.text == 'секрет')
async def secret(message: Message):
    await  message.answer('Секретная информация')

@router.message(F.text == '📋 Мои задания')
async def list_tasks(message: Message):
    await message.answer('Вот ваш список заданий:\n2. Выучить SQLAlchemy')

@router.message(F.text == '➕ Создать задачу')
async def add_task(message: Message, state:FSMContext):
    await state.set_state(AddTask.title)
    await message.answer("Введите название задачи")

@router.message(AddTask.title)
async def add_task_second(message:Message, state:FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddTask.description)
    await message.answer("Введите описание")

@router.message(AddTask.description)
async def add_task_third(message:Message, state:FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddTask.priority)
    await message.answer("Какой приоритет у этой задачи?")

@router.message(AddTask.priority)
async def add_task_fourth(message:Message, state:FSMContext):
    await state.update_data(priority = message.text)
    data = await state.get_data()
    await message.answer(f"Новая задача создана!\nНазвание задачи:{data["title"]}"
                         f"\nОписание:{data["description"]}"
                         f"\nПриоритет:{data["priority"]}")
    await state.clear()