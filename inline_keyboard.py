from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

BTN_TODAY = InlineKeyboardButton('Сегодня \U0001F4B8', callback_data='today')
BTN_MONTH = InlineKeyboardButton('Месяц \U0001F4B0', callback_data='month')
BTN_EXPENSES = InlineKeyboardButton('Последнее \U0001F9FE', callback_data='expenses')
BTN_CATEGORIES = InlineKeyboardButton('Категории \U0001F5D2', callback_data='categories')

# START = ReplyKeyboardMarkup().add(BTN_START)

TODAY = InlineKeyboardMarkup().add(BTN_MONTH, BTN_EXPENSES, BTN_CATEGORIES)
MONTH = InlineKeyboardMarkup().add(BTN_TODAY, BTN_EXPENSES, BTN_CATEGORIES)
EXPENSES = InlineKeyboardMarkup().add(BTN_TODAY, BTN_MONTH, BTN_CATEGORIES)
CATEGORIES = InlineKeyboardMarkup().add(BTN_TODAY, BTN_MONTH, BTN_EXPENSES)
ALL = InlineKeyboardMarkup().add(BTN_TODAY, BTN_MONTH, BTN_EXPENSES, BTN_CATEGORIES)