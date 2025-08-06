import asyncio
from aiogram import Router, Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from database import init_db, is_logged, check_user, username_exists, set_logged, register_user
from aiogram.client.default import DefaultBotProperties
from state import RegisterState, LoginState
from keyboards import main_kb

token='8402130086:AAHi-6DzcZ1t8271c5dqqbZ9hrzeA9PzL9g'

dp = Dispatcher()
router = Router()

bot = Bot(token=token)


@router.message(CommandStart())
async def cmd_str(message: Message):
    await message.answer('Привет! Используй /register или /login')



@router.message(Command('register'))
async def cmd_register(message: Message, state: FSMContext):
    await message.answer('Введите username: ')
    await state.set_data(RegisterState.username)


@router.message(RegisterState.username)
async def reg_get_username(message: Message, state: FSMContext):
    username = message.text
    if username_exists(username):
        return await message.answer('Такой username уже занят. Выберите другой: ')
    await state.update_data(username=username)
    await message.answer('Введите пароль: ')
    await state.set_state(RegisterState.password)

@router.message(RegisterState.password)
async def reg_password(message: Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    password = message.text
    register_user(username, password, message.from_user.id)
    await state.clear()
    await message.answer('Регистрация Завершена ✅ Вы вошли', reply_markup=main_kb)

@router.message(Command('login'))
async def cmd_login(message: Message, state: FSMContext):
    await message.answer('Введите username: ')
    await state.set_data(LoginState.username)

@router.message(LoginState.username)
async def login_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Введите password: ')
    await state.set_state(LoginState.password)

@router.message(LoginState.password)
async def login_password(message: Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    password = message.text
    a, b = check_user(username, password)
    if not a or b != message.from_user_id:
        await state.clear()
        return await message.answer('Неверные данные')
    set_logged(message.from_user.id, 1)
    await state.clear()
    await message.answer('Успешный вход', reply_markup=main_kb)


