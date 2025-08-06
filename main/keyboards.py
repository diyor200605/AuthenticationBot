from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Профиль'), KeyboardButton(text='Выйти'),
         KeyboardButton(text='Войти')]
    ],
    resize_keyboard=True
)